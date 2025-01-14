class baseMan 
{
	displayName = "Unarmed";
	// All Randomized
	uniform[] = 
	{
		"aegis_ccu_mtp",
		"aegis_ccu_rs_mtp",
		"aegis_ccu_tshirt_mtp"
	};
	vest[] = 
	{
		"aegis_platecarrier_rig_khk"
	};
	backpack[] = 
	{
		"aegis_assaultpack_mtp"
	};
	headgear[] = 
	{
		"aegis_ech_enh_mtp"	
	};
	goggles[] = {};
	hmd[] = {};
	// Leave empty to not change faces and Insignias
	faces[] = {};
	insignias[] = {};
	// All Randomized. Add Primary Weapon and attachments
	// Leave Empty to remove all. {"Default"} for using original items the character start with
	primaryWeapon[] = {};
	scope[] = {};
	bipod[] = {};
	attachment[] = {};
	silencer[] = {};
	// SecondaryAttachments[] arrays are NOT randomized
	secondaryWeapon[] = {};
	secondaryAttachments[] = {};
	sidearmWeapon[] = {};
	sidearmAttachments[] = {};
	// These are added to the uniform or vest first - overflow goes to backpack if there's any
	magazines[] = {};
	items[] =
	{
		"ACRE_PRC343",
		LIST_10("ACE_fieldDressing"),
		LIST_10("ACE_packingBandage"),
		LIST_4("ACE_tourniquet"),
		LIST_2("ACE_epinephrine"),
		LIST_2("ACE_morphine"),
		LIST_2("ACE_splint")
	};
	// These are added directly into their respective slots
	linkedItems[] = 
	{
		"ItemWatch",
		"ItemMap",
		"ItemCompass",
		"ItemGPS"
	};
	// These are put directly into the backpack
	backpackItems[] = {};
	// This is executed after the unit init is complete. Argument: _this = _unit
	code = "";
};

class rm : baseMan
{
	displayName = "Rifleman";
	primaryWeapon[] = 
	{
		"rhs_weap_vhsd2_ct15x"
	};
	bipod[] =
	{
		"rhsusf_acc_rvg_blk"
	};
	sidearmWeapon[] =
	{
		"rhsusf_weap_glock17g4"
	};
	magazines[] = 
	{
		LIST_2("SmokeShell"),
		LIST_2("HandGrenade"),
		LIST_9("rhsgref_30rnd_556x45_vhs2"),
		LIST_2("rhsusf_mag_17Rnd_9x19_FMJ")
	};
};

class ar : rm 
{
	displayName = "Automatic Rifleman";
	backpack[] = 
	{
		"aegis_carryall_mtp"
	};
	primaryWeapon[] = 
	{
		"rhs_weap_m249_light_L"
	};
	scope[] =
	{
		"optic_MRCO"
	};
	bipod[] = 
	{
		"rhsusf_acc_grip4_bipod"
	};
	magazines[] = 
	{
		LIST_2("SmokeShell"),
		LIST_2("HandGrenade"),
		LIST_2("rhsusf_mag_17Rnd_9x19_FMJ"),
		LIST_3("rhsusf_200Rnd_556x45_mixed_soft_pouch")
	};
	backpackItems[] = 
	{
		LIST_4("rhsusf_200Rnd_556x45_mixed_soft_pouch")
	};
};

class aar : rm 
{
	displayName = "Assistant Automatic Rifleman";
	backpack[] = 
	{
		"aegis_carryall_mtp"
	};
	backpackItems[] += 
	{
		LIST_4("rhsusf_200Rnd_556x45_mixed_soft_pouch")
	};
	linkedItems[] += 
	{
		"ACE_Vector"
	};
};

class rm_lat : rm 
{
	displayName = "Rifleman (AT)";
	backpack[] = 
	{
		"aegis_carryall_mtp"
	};	
	secondaryWeapon[] = 
	{
		"rhs_weap_smaw_green"
	};
	secondaryAttachments[] =
	{
		"rhs_weap_optic_smaw"
	};	
	magazines[] = 
	{
		LIST_2("SmokeShell"),
		LIST_2("HandGrenade"),
		LIST_6("rhsgref_30rnd_556x45_vhs2"),
		"rhsusf_mag_17Rnd_9x19_FMJ"
	};	
	backpackItems[] = 
	{
		LIST_2("rhs_mag_smaw_SR"),
		LIST_2("rhs_mag_smaw_HEAA")
	};
};

class tl : rm 
{
	displayName = "Team Leader";
	primaryWeapon[] = 
	{
		"rhs_weap_vhsd2_bg_ct15x"
	};	
	magazines[] = 
	{
		LIST_2("SmokeShell"),
		LIST_2("HandGrenade"),
		LIST_9("rhsgref_30rnd_556x45_vhs2_T"),
		LIST_2("rhsusf_mag_17Rnd_9x19_FMJ")
	};	
	backpackItems[] = 
	{
		LIST_16("rhs_mag_M441_HE"),
		LIST_15("rhs_mag_M433_HEDP"),
		LIST_5("1Rnd_Smoke_Grenade_shell")
	};
	linkedItems[] += 
	{
		"ACE_Vector"
	};
};

class sl : tl 
{
	displayName = "Squad Leader";
	items[] += 
	{
		"ACRE_PRC148"
	};
	backpackItems[] =
	{
		LIST_21("rhs_mag_M441_HE"),
		LIST_10("rhs_mag_M433_HEDP"),
		LIST_6("1Rnd_Smoke_Grenade_shell"),
		LIST_4("1Rnd_SmokeBlue_Grenade_shell"),
		LIST_4("1Rnd_SmokeRed_Grenade_shell"),
		LIST_5("rhsgref_30rnd_556x45_vhs2_t")		
	};
};

class co : sl 
{
	displayName = "Platoon Commander";
};

class sgt : sl 
{
	displayName = "Platoon Sergeant";
};

class fac : sl 
{
	displayName = "Forward Air Controller";
	backpackItems[] =
	{
		"Laserbatteries",
		LIST_11("rhs_mag_M441_HE"),
		LIST_4("1Rnd_Smoke_Grenade_shell"),
		LIST_4("1Rnd_SmokeBlue_Grenade_shell"),
		LIST_4("1Rnd_SmokeGreen_Grenade_shell"),
		LIST_4("1Rnd_SmokeRed_Grenade_shell"),
		LIST_2("SmokeShellBlue"),
		LIST_2("SmokeShellGreen"),
		LIST_2("SmokeShellRed")
	};
	linkedItems[] += 
	{
		"Laserdesignator_03"
	};
};

class rm_fa : rm 
{
	displayName = "Rifleman (First-Aid)";
	traits[] = {"medic"};
	backpack[] = 
	{
		"aegis_tacticalpack_mtp"
	};
	backpackItems[] =
	{
		LIST_20("ACE_fieldDressing"),
		LIST_15("ACE_packingBandage"),
		LIST_15("ACE_elasticBandage"),
		LIST_10("ACE_epinephrine"),
		LIST_10("ACE_morphine"),
		LIST_8("ACE_bloodIV"),
		LIST_4("ACE_splint"),
		LIST_4("ACE_tourniquet"),
		LIST_2("ACE_adenosine")
	};
};

class cls : rm_fa
{
	displayName = "Combat Life Saver";
	backpackItems[] =
	{
		"ACE_surgicalKit",
		LIST_30("ACE_elasticBandage"),
		LIST_30("ACE_packingBandage"),
		LIST_20("ACE_fieldDressing"),
		LIST_20("ACE_epinephrine"),
		LIST_20("ACE_morphine"),
		LIST_12("ACE_bloodIV"),
		LIST_10("ACE_splint"),
		LIST_4("ACE_tourniquet"),
		LIST_2("ACE_adenosine")
	};
};

class mmg : ar 
{
	displayName = "Medium Machine Gunner";
	primaryWeapon[] = 
	{
		"rhs_weap_m240B"
	};
	scope[]= 
	{
		"rhsusf_acc_ACOG_MDO"
	};
	bipod[] = {};
	attachment[] = {};
	silencer[] = 
	{
		"rhsusf_acc_ARDEC_M240"
	};
	magazines[] = 
	{
		LIST_2("SmokeShell"),
		LIST_2("HandGrenade"),
		LIST_2("rhsusf_mag_17Rnd_9x19_FMJ"),
		LIST_3("rhsusf_100Rnd_762x51_m80a1epr")
	};
	backpackItems[] = 
	{
		LIST_6("rhsusf_100Rnd_762x51_m80a1epr")
	};
};

class ammg : aar 
{
	displayName = "Assistant Medium Machine Gunner";
	backpackItems[] = 
	{
		LIST_8("rhsusf_100Rnd_762x51_m80a1epr")
	};
};

class mat : rm_lat 
{
	displayName = "Heavy Anti-Tank Gunner";
	secondaryWeapon[] = 
	{
		"rhs_weap_fgm148"
	};
	backpackItems[] = 
	{
		"rhs_fgm148_magazine_AT"
	};
};

class amat : rm 
{
	displayName = "Assistant Heavy Anti-Tank Gunner";
	backpack[] = 
	{
		"aegis_carryall_mtp"
	};
	backpackItems[] = 
	{
		"rhs_fgm148_magazine_AT"
	};
	linkedItems[] += 
	{
		"ACE_Vector"
	};
};

class crew : rm 
{
	displayName = "Crewman";
	traits[] = {"engineer"};
	vest[] = 
	{
		"aegis_platecarrier_lite_khk"
	};
	headgear[] = 
	{
		"H_HelmetCrew_I"
	};
	primaryWeapon[] =
	{
		"rhs_weap_vhsk2"
	};	
	backpackItems[] = 
	{
		"ToolKit"
	};
};

class crew_co : crew 
{
	displayName = "Crewman Commander";
	items[] +=
	{
		"ACRE_PRC148"
	};
	linkedItems[] +=
	{
		"ACE_Vector"
	};
};

class hp : rm
{
	displayName = "Helicopter Pilot";
	traits[] = {"engineer"};
	vest[] = 
	{
		"aegis_platecarrier_lite_khk"
	};
	headgear[] = 
	{
		"rhsusf_hgu56p_visor"
	};
	primaryWeapon[] =
	{
		"rhs_weap_vhsk2"
	};
	items[] +=
	{
		"ACRE_PRC148"
	};	
	backpackItems[] = 
	{
		"ToolKit"
	};	
};

class eng : rm 
{
	displayName = "Engineer";
	traits[] = {"engineer","explosiveSpecialist"};
	backpack[] = 
	{
		"aegis_carryall_mtp"
	};
	backpackItems[] = 
	{
		"ToolKit",
		"ACE_DefusalKit",
		"ACE_M26_Clacker",
		"ACE_wirecutter",
		LIST_4("rhsusf_m112_mag"),
		LIST_2("rhsusf_m112x4_mag")
	};
};

//********************************************************************************//
//Uncommon Roles - !!! CUSTOM ENTRIES NEEDED FOR CURATED ARSENAL !!!
//********************************************************************************//

class jp : rm 
{
	displayName = "Jet Pilot";
	uniform[] = 
	{
		"U_I_pilotCoveralls"
	};
	vest[] = 
	{
		"pca_vest_invisible_plate"
	};
	headgear[] = 
	{
		"H_PilotHelmetFighter_O"
	};
	backpack[] = 
	{
		"B_Parachute"
	};
	items[] +=
	{
		"ACRE_PRC148"
	};
	primaryWeapon[] = {};
	sidearmWeapon[] = 
	{
		"rhsusf_weap_glock17g4"
	};
	magazines[] = 
	{
		LIST_2("SmokeShell"),
		LIST_5("rhsusf_mag_17Rnd_9x19_FMJ"),
		LIST_2("SmokeShellBlue"),
		LIST_2("SmokeShellGreen"),
		LIST_2("SmokeShellRed")
	};
	backpackItems[] = {};
};

class sn : rm 
{
	displayName = "Sniper";
	headgear[] =
	{
		"aegis_ech_ghillie_mtp"
	};	
	vest[] =
	{
		"aegis_platecarrier_lite_khk"
	};
	backpack[] = 
	{
		"aegis_tacticalpack_mtp"
	};	
	primaryWeapon[] = 
	{
		"rhs_weap_M107"
	};
	scope[] = 
	{
		"rhsusf_acc_nxs_3515x50f1_md_sun"
	};
	attachment[] = {""};
	bipod[] = {""};
	items[] +=
	{
		"ACE_ATragMX",
		"ACE_microDAGR"
	};
	magazines[] = 
	{
		LIST_2("SmokeShell"),
		LIST_2("HandGrenade"),
		LIST_4("rhsusf_mag_10Rnd_STD_50BMG_M33"),
		LIST_2("rhsusf_mag_17Rnd_9x19_FMJ")
	};
	backpackItems[] = 
	{
		LIST_2("rhsusf_mag_10Rnd_STD_50BMG_M33"),
		LIST_2("rhsusf_mag_10Rnd_STD_50BMG_mk211")
	};
	linkedItems[] += 
	{
		"ACE_Vector"
	};
};

class spt : sl 
{
	displayName = "Spotter";
	headgear[] =
	{
		"aegis_ech_ghillie_mtp"
	};
	vest[] =
	{
		"aegis_platecarrier_lite_khk"
	};	
	backpack[] = 
	{
		"aegis_tacticalpack_mtp"
	};	
	primaryWeapon[] = 
	{
		"rhs_weap_vhsd2_bg"
	};
	scope[] = 
	{
		"rhsusf_acc_su230"
	};
	items[] +=
	{
		"ACE_ATragMX",
		"ACE_microDAGR"
	};	
	backpackItems[] = 
	{
		LIST_11("rhs_mag_M441_HE"),
		LIST_10("rhs_mag_M433_HEDP"),
		LIST_6("1Rnd_Smoke_Grenade_shell"),		
		"ACE_SpottingScope",
		"ACE_Tripod",
		"ACE_HuntIR_monitor",
		LIST_5("ACE_HuntIR_M203")
	};
};