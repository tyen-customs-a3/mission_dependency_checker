from typing import List, Dict, Set, NamedTuple
from mission_dependency_scanner import MissionDependencyScanner
import logging

logger = logging.getLogger(__name__)

class ComparisonResult(NamedTuple):
    mission_name: str
    task1_name: str
    task2_name: str
    missing_classes1: Set[str]
    missing_classes2: Set[str]
    unique_to_task1: Set[str]
    unique_to_task2: Set[str]
    common_missing: Set[str]
    missing_assets1: Set[str]
    missing_assets2: Set[str]

def compare_task_results(task1_name: str, task1_reports: List[MissionDependencyScanner],
                        task2_name: str, task2_reports: List[MissionDependencyScanner]) -> List[ComparisonResult]:
    """Compare results between two scan tasks"""
    
    # Create mission name lookup
    task1_missions = {scanner.mission_name: scanner for scanner in task1_reports}
    task2_missions = {scanner.mission_name: scanner for scanner in task2_reports}
    
    all_missions = sorted(set(task1_missions.keys()) | set(task2_missions.keys()))
    results = []
    
    for mission_name in all_missions:
        scanner1 = task1_missions.get(mission_name)
        scanner2 = task2_missions.get(mission_name)
        
        missing_classes1 = scanner1.missing_classes if scanner1 else set()
        missing_classes2 = scanner2.missing_classes if scanner2 else set()
        
        missing_assets1 = scanner1.missing_assets if scanner1 else set()
        missing_assets2 = scanner2.missing_assets if scanner2 else set()
        
        # Find unique issues in each task
        unique_to_task1 = missing_classes1 - missing_classes2
        unique_to_task2 = missing_classes2 - missing_classes1
        common_missing = missing_classes1 & missing_classes2
        
        results.append(ComparisonResult(
            mission_name=mission_name,
            task1_name=task1_name,
            task2_name=task2_name,
            missing_classes1=missing_classes1,
            missing_classes2=missing_classes2,
            unique_to_task1=unique_to_task1,
            unique_to_task2=unique_to_task2,
            common_missing=common_missing,
            missing_assets1=missing_assets1,
            missing_assets2=missing_assets2
        ))
    
    return results
