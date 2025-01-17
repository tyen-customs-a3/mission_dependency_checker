import os
import json
from typing import Dict, Set, List, Tuple
import xml.sax.saxutils as saxutils
from database_types import ClassEntry
from database_class import parse_inidbi2_file
from concurrent.futures import ThreadPoolExecutor
from threading import Lock
import logging
from queue import Queue
import itertools

logger = logging.getLogger(__name__)

# Thread-safe counter for tracking progress
class AtomicCounter:
    def __init__(self):
        self._counter = 0
        self._lock = Lock()

    def increment(self):
        with self._lock:
            self._counter += 1
            return self._counter

    def value(self):
        return self._counter

def _process_node_batch(batch: List[ClassEntry], processed_nodes: Set[str]) -> List[dict]:
    """Process a batch of nodes in parallel"""
    nodes = []
    for entry in batch:
        if entry.class_name not in processed_nodes:
            node = {
                'id': entry.class_name,
                'label': entry.class_name,
                'group': entry.source,
                'properties': {
                    'source': entry.source,
                    'category': entry.category,
                    'isSimpleObject': entry.is_simple_object,
                    'numProperties': entry.num_properties,
                    'scope': entry.scope,
                    'model': entry.model,
                    'displayName': entry.display_name
                }
            }
            nodes.append(node)
    return nodes

def _process_edge_batch(batch: List[ClassEntry]) -> List[dict]:
    """Process a batch of edges in parallel"""
    edges = []
    for entry in batch:
        if entry.parent:
            edges.append({
                'from': entry.class_name,
                'to': entry.parent,
                'type': 'parent'
            })
        if entry.inherits_from and entry.inherits_from != entry.parent:
            edges.append({
                'from': entry.class_name,
                'to': entry.inherits_from,
                'type': 'inherits'
            })
    return edges

def create_node_edge_structure(classes: Dict[str, Set[ClassEntry]], 
                             max_workers: int = None,
                             batch_size: int = 100) -> Tuple[List[dict], List[dict]]:
    """Convert class database into nodes and edges using parallel processing"""
    logger.info("Starting node and edge structure creation...")
    logger.info(f"Using {max_workers} workers and batch size of {batch_size}")
    
    if max_workers is None:
        max_workers = min(32, (os.cpu_count() or 1) + 4)

    processed_nodes = set()
    nodes = []
    edges = []
    counter = AtomicCounter()
    
    # Flatten all entries for batch processing
    logger.info("Flattening class entries...")
    all_entries = list(itertools.chain.from_iterable(classes.values()))
    total_entries = len(all_entries)
    logger.info(f"Total entries to process: {total_entries:,}")
    
    # Create batches
    node_batches = [all_entries[i:i + batch_size] 
                   for i in range(0, len(all_entries), batch_size)]
    logger.info(f"Created {len(node_batches)} batches for processing")
    
    # Process nodes in parallel
    logger.info("Starting parallel node processing...")
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit node processing tasks
        future_to_batch = {
            executor.submit(_process_node_batch, batch, processed_nodes): batch 
            for batch in node_batches
        }
        
        # Collect node results
        for future in future_to_batch:
            try:
                batch_nodes = future.result()
                nodes.extend(batch_nodes)
                for node in batch_nodes:
                    processed_nodes.add(node['id'])
                completed = counter.increment()
                if completed % 10 == 0:  # Log progress every 10 batches
                    logger.info(f"Processed {completed}/{len(node_batches)} node batches")
            except Exception as e:
                logger.error(f"Error processing node batch: {e}")
    
    logger.info(f"Completed node processing. Generated {len(nodes):,} nodes")
    
    # Reset counter for edge processing
    counter = AtomicCounter()
    
    # Process edges in parallel
    logger.info("Starting parallel edge processing...")
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit edge processing tasks
        future_to_batch = {
            executor.submit(_process_edge_batch, batch): batch 
            for batch in node_batches
        }
        
        # Collect edge results
        for future in future_to_batch:
            try:
                batch_edges = future.result()
                edges.extend(batch_edges)
                completed = counter.increment()
                if completed % 10 == 0:  # Log progress every 10 batches
                    logger.info(f"Processed {completed}/{len(node_batches)} edge batches")
            except Exception as e:
                logger.error(f"Error processing edge batch: {e}")
    
    logger.info(f"Completed edge processing. Generated {len(edges):,} edges")
    logger.info(f"Completed processing {total_entries} entries")
    return nodes, edges

def export_to_json(classes: Dict[str, Set[ClassEntry]], output_file: str, max_workers: int = None):
    """Export class hierarchy to JSON format suitable for visualization"""
    nodes, edges = create_node_edge_structure(classes, max_workers)
    
    graph_data = {
        'nodes': nodes,
        'edges': edges
    }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(graph_data, f, indent=2)

def _process_graphml_node(node: dict) -> List[str]:
    """Process a single node into GraphML format"""
    escaped_id = saxutils.escape(node["id"])
    escaped_label = saxutils.escape(node["label"])
    escaped_group = saxutils.escape(node["group"])
    
    node_lines = [f'    <node id="{escaped_id}">',
                 f'      <data key="label">{escaped_label}</data>',
                 f'      <data key="group">{escaped_group}</data>']
    
    # Add all properties
    props = node["properties"]
    node_lines.extend([
        f'      <data key="source">{saxutils.escape(str(props["source"]))}</data>',
        f'      <data key="category">{saxutils.escape(str(props["category"]))}</data>',
        f'      <data key="isSimpleObject">{str(props["isSimpleObject"]).lower()}</data>',
        f'      <data key="numProperties">{props["numProperties"]}</data>',
        f'      <data key="scope">{props["scope"]}</data>'
    ])
    
    # Add optional properties if they exist
    if props["model"]:
        node_lines.append(f'      <data key="model">{saxutils.escape(props["model"])}</data>')
    if props["displayName"]:
        node_lines.append(f'      <data key="displayName">{saxutils.escape(props["displayName"])}</data>')
        
    node_lines.append('    </node>')
    return node_lines

def _process_graphml_edge(edge: dict) -> str:
    """Process a single edge into GraphML format"""
    return (f'    <edge source="{saxutils.escape(edge["from"])}" '
            f'target="{saxutils.escape(edge["to"])}">'
            f'      <data key="type">{saxutils.escape(edge["type"])}</data>'
            f'    </edge>')

def export_to_graphml(classes: Dict[str, Set[ClassEntry]], output_file: str, max_workers: int = None):
    """Export class hierarchy to GraphML format using parallel processing"""
    logger.info(f"Starting GraphML export to {output_file}")
    nodes, edges = create_node_edge_structure(classes, max_workers)
    
    # First collect all referenced nodes from edges to ensure they exist
    logger.info("Checking for missing node references...")
    referenced_nodes = set()
    for edge in edges:
        referenced_nodes.add(edge['from'])
        referenced_nodes.add(edge['to'])
    
    # Add placeholder nodes for any missing references
    existing_node_ids = {node['id'] for node in nodes}
    missing_nodes = referenced_nodes - existing_node_ids
    if missing_nodes:
        logger.info(f"Adding {len(missing_nodes)} placeholder nodes for missing references")
        for node_id in missing_nodes:
            nodes.append({
                'id': node_id,
                'label': node_id,
                'group': 'unknown',
                'properties': {
                    'source': 'unknown',
                    'category': 'unknown',
                    'isSimpleObject': False,
                    'numProperties': 0,
                    'scope': 0,
                    'model': None,
                    'displayName': None
                }
            })
    
    # Calculate node levels for hierarchical layout
    logger.info("Calculating hierarchical layout levels...")
    node_levels = {}
    def calculate_level(node_id: str, visited: Set[str] = None) -> int:
        if visited is None:
            visited = set()
        if node_id in visited:
            return node_levels.get(node_id, 0)
        visited.add(node_id)
        
        # Find all parent edges for this node
        parent_edges = [e for e in edges if e['from'] == node_id]
        if not parent_edges:
            node_levels[node_id] = 0
            return 0
        
        # Calculate maximum level of parents
        max_parent_level = 0
        for edge in parent_edges:
            if edge['to'] not in visited:
                parent_level = calculate_level(edge['to'], visited)
                max_parent_level = max(max_parent_level, parent_level)
        
        level = max_parent_level + 1
        node_levels[node_id] = level
        return level

    # Calculate levels for all nodes
    for node in nodes:
        if node['id'] not in node_levels:
            calculate_level(node['id'])
    
    # Create GraphML header with yFiles layout extension
    xml_lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<graphml xmlns="http://graphml.graphdrawing.org/xmlns"',
        '         xmlns:y="http://www.yworks.com/xml/graphml">',
        '  <key id="label" for="node" attr.name="label" attr.type="string"/>',
        '  <key id="group" for="node" attr.name="group" attr.type="string"/>',
        '  <key id="source" for="node" attr.name="source" attr.type="string"/>',
        '  <key id="category" for="node" attr.name="category" attr.type="string"/>',
        '  <key id="isSimpleObject" for="node" attr.name="isSimpleObject" attr.type="boolean"/>',
        '  <key id="numProperties" for="node" attr.name="numProperties" attr.type="int"/>',
        '  <key id="scope" for="node" attr.name="scope" attr.type="int"/>',
        '  <key id="model" for="node" attr.name="model" attr.type="string"/>',
        '  <key id="displayName" for="node" attr.name="displayName" attr.type="string"/>',
        '  <key id="level" for="node" attr.name="level" attr.type="int"/>',
        '  <key id="type" for="edge" attr.name="type" attr.type="string"/>',
        '  <key id="y:NodeLabel" for="node" attr.name="NodeLabel" attr.type="string"/>',
        '  <key id="y:EdgeLabel" for="edge" attr.name="EdgeLabel" attr.type="string"/>',
        '  <key id="y:Shape" for="node" attr.name="Shape" attr.type="string"/>',
        '  <graph id="G" edgedefault="directed">'
    ]

    def _process_hierarchical_node(node: dict) -> List[str]:
        """Process a node with hierarchical layout information"""
        escaped_id = saxutils.escape(node["id"])
        escaped_label = saxutils.escape(node["label"])
        escaped_group = saxutils.escape(node["group"])
        level = node_levels.get(node["id"], 0)
        
        node_lines = [
            f'    <node id="{escaped_id}">',
            f'      <data key="label">{escaped_label}</data>',
            f'      <data key="group">{escaped_group}</data>',
            f'      <data key="level">{level}</data>',
            f'      <data key="y:NodeLabel">{escaped_label}</data>',
            f'      <data key="y:Shape">rectangle</data>'
        ]
        
        # Add all properties
        props = node["properties"]
        node_lines.extend([
            f'      <data key="source">{saxutils.escape(str(props["source"]))}</data>',
            f'      <data key="category">{saxutils.escape(str(props["category"]))}</data>',
            f'      <data key="isSimpleObject">{str(props["isSimpleObject"]).lower()}</data>',
            f'      <data key="numProperties">{props["numProperties"]}</data>',
            f'      <data key="scope">{props["scope"]}</data>'
        ])
        
        # Add optional properties if they exist
        if props["model"]:
            node_lines.append(f'      <data key="model">{saxutils.escape(props["model"])}</data>')
        if props["displayName"]:
            node_lines.append(f'      <data key="displayName">{saxutils.escape(props["displayName"])}</data>')
        
        node_lines.append('    </node>')
        return node_lines

    def _process_hierarchical_edge(edge: dict) -> str:
        """Process an edge with layout information"""
        return (
            f'    <edge source="{saxutils.escape(edge["from"])}" '
            f'target="{saxutils.escape(edge["to"])}">'
            f'      <data key="type">{saxutils.escape(edge["type"])}</data>'
            f'      <data key="y:EdgeLabel">{saxutils.escape(edge["type"])}</data>'
            f'    </edge>'
        )
    
    # Process all nodes first with hierarchical information
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        logger.info("Processing nodes with hierarchical layout...")
        node_futures = list(executor.map(lambda n: _process_hierarchical_node(n), nodes))
        xml_lines.extend(itertools.chain.from_iterable(node_futures))
    
    # Then process all edges with layout information
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        logger.info("Processing edges with layout information...")
        edge_futures = list(executor.map(lambda e: _process_hierarchical_edge(e), edges))
        xml_lines.extend(edge_futures)
    
    # Add closing tags
    xml_lines.extend(['  </graph>', '</graphml>'])
    
    logger.info("Writing file to disk...")
    # Write to file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(xml_lines))
    
    logger.info(f"Export complete. Written to {output_file}")
    logger.info(f"Final statistics: {len(nodes):,} nodes, {len(edges):,} edges")

def main():
    """Main function to demonstrate usage"""
    import argparse
    
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%H:%M:%S'
    )
    
    parser = argparse.ArgumentParser(description='Export class hierarchy to various formats')
    parser.add_argument('ini_file', help='Path to INIDBI2 ini file')
    parser.add_argument('output_file', help='Output file path')
    parser.add_argument('--format', choices=['json', 'graphml'], default='json',
                       help='Output format (default: json)')
    parser.add_argument('--max-workers', type=int, default=None, help='Maximum number of worker threads')
    
    args = parser.parse_args()
    
    logger.info(f"Starting export process for {args.ini_file}")
    logger.info(f"Output format: {args.format}")
    
    # Parse the ini file
    logger.info("Parsing input file...")
    classes = parse_inidbi2_file(args.ini_file)
    logger.info(f"Found {sum(len(s) for s in classes.values()):,} total classes")
    
    # If max workers is not specified use CPU count
    if args.max_workers is None:
        args.max_workers = max(1, os.cpu_count() - 1)

    # Export to specified format
    if args.format == 'json':
        export_to_json(classes, args.output_file, args.max_workers)
    else:
        export_to_graphml(classes, args.output_file, args.max_workers)
    
    logger.info("Export process completed successfully")

if __name__ == '__main__':
    main()
