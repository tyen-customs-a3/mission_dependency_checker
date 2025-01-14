////////////////////////////////////////////////////////////////////
//DeRap: config.bin
//Produced from mikero's Dos Tools Dll version 9.93
//https://mikero.bytex.digital/Downloads
//'now' is Tue Jan 14 10:03:29 2025 : 'file' last modified on Mon Feb 28 19:03:47 2022
////////////////////////////////////////////////////////////////////

#define _ARMA_

class CfgPatches
{
	class A3_Aegis_Weapons_F_Aegis
	{
		author = "AveryTheKitty";
		name = "Arma 3 Aegis - Weapons and Accessories";
		url = "https://steamcommunity.com/sharedfiles/filedetails/?id=949252631";
		requiredAddons[] = {"A3_Aegis_Data_F_Aegis","A3_Sounds_F","A3_Sounds_F_Tank","A3_Weapons_F","A3_Weapons_F_Enoch","A3_Weapons_F_Exp","A3_Weapons_F_Mark","A3_Weapons_F_Orange","cba_jr","cba_jr_prep","rhs_c_weapons"};
		requiredVersion = 0.1;
		units[] = {};
		weapons[] = {"aegis_weap_aur90","aegis_weap_aur90_tan","aegis_weap_aur90_eglm","aegis_weap_aur90_eglm_tan","aegis_weap_aur90_carbine","aegis_weap_aur90_carbine_tan","aegis_weap_sa80_blk","aegis_weap_sa80_eglm_blk","aegis_weap_sa80c_blk","aegis_weap_sa80_khk","aegis_weap_sa80_eglm_khk","aegis_weap_sa80c_khk","aegis_weap_sa80_sand","aegis_weap_sa80_eglm_sand","aegis_weap_sa80c_sand","aegis_weap_g36k_65_blk","aegis_weap_g36k_gl_65_blk","aegis_weap_g36c_65_blk","aegis_weap_vs121_blk","aegis_weap_m14_blk","aegis_weap_f2000_blk","aegis_weap_f2000c_blk","aegis_weap_f2000_gl_blk","aegis_weap_ncar15_blk","aegis_weap_ncar15_gl_blk","aegis_weap_ncar15_carbine_blk","aegis_weap_ncar15_lsw_blk","aegis_weap_mraws_blk","aegis_weap_mraws_rail_blk","aegis_weap_rpg32_blk","aegis_weap_rpg32_camo","aegis_acc_lrco_blk","aegis_acc_lrco_sand","nvg_goggles_cbr","nvg_goggles_grn","nvg_goggles_tropic","nvg_scrim_wdl","nvg_scrim_wdl_grass","nvg_scrim_wdl_leaves_1","nvg_scrim_wdl_leaves_2","nvg_scrim_wdl_leaves_3","nvg_scrim_wdl_pine","nvg_scrim_snow","nvg_scrim_snow_pine"};
		magazines[] = {};
		ammo[] = {};
	};
};
class CfgMovesBasic
{
	class Default;
	class ManActions
	{
		GestureReloadAUG = "GestureReloadAUG";
		GestureReloadSA80 = "GestureReloadSA80";
		GestureReloadG36 = "GestureReloadG36";
	};
	class Actions
	{
		class NoActions: ManActions
		{
			GestureReloadAUG[] = {"GestureReloadAUG","Gesture"};
			GestureReloadSA80[] = {"GestureReloadSA80","Gesture"};
			GestureReloadG36[] = {"GestureReloadG36","Gesture"};
		};
		class RifleBaseStandActions;
		class RifleProneActions: RifleBaseStandActions
		{
			GestureReloadAUG[] = {"GestureReloadAUGProne","Gesture"};
			GestureReloadSA80[] = {"GestureReloadSA80Prone","Gesture"};
			GestureReloadG36[] = {"GestureReloadSA80Prone","Gesture"};
		};
		class RifleAdjustProneBaseActions;
		class RifleAdjustFProneActions: RifleAdjustProneBaseActions
		{
			GestureReloadAUG[] = {"GestureReloadAUGContext","Gesture"};
			GestureReloadSA80[] = {"GestureReloadSA80Context","Gesture"};
			GestureReloadG36[] = {"GestureReloadSA80Context","Gesture"};
		};
		class RifleAdjustLProneActions: RifleAdjustProneBaseActions
		{
			GestureReloadAUG[] = {"GestureReloadAUGContext","Gesture"};
			GestureReloadSA80[] = {"GestureReloadSA80Context","Gesture"};
			GestureReloadG36[] = {"GestureReloadSA80Context","Gesture"};
		};
		class RifleAdjustRProneActions: RifleAdjustProneBaseActions
		{
			GestureReloadAUG[] = {"GestureReloadAUGContext","Gesture"};
			GestureReloadSA80[] = {"GestureReloadSA80Context","Gesture"};
			GestureReloadG36[] = {"GestureReloadSA80Context","Gesture"};
		};
		class PistolStandActions;
		class PistolProneActions: PistolStandActions
		{
			GestureReloadAUG[] = {"GestureReloadAUGProne","Gesture"};
			GestureReloadSA80[] = {"GestureReloadSA80Prone","Gesture"};
			GestureReloadG36[] = {"GestureReloadSA80Prone","Gesture"};
		};
		class DeployedProneActions: RifleProneActions
		{
			GestureReloadAUG[] = {"GestureReloadAUGProne","Gesture"};
			GestureReloadSA80[] = {"GestureReloadSA80Prone","Gesture"};
			GestureReloadG36[] = {"GestureReloadG36Prone","Gesture"};
		};
	};
};
class CfgGesturesMale
{
	class Default;
	class States
	{
		class GestureReloadBase;
		class GestureReloadAUG: GestureReloadBase
		{
			file = "\a3_aegis\weapons_f_aegis\data\anim\GestureReloadAUG.rtm";
			speed = 0.18;
			mask = "handsWeapon";
			headBobStrength = 0.22;
			headBobMode = 2;
			weaponIK = 1;
			leftHandIKCurve[] = {0,1,0.036,0,0.836,0,0.873,1};
		};
		class GestureReloadAUGProne: GestureReloadAUG
		{
			file = "\a3_aegis\weapons_f_aegis\data\anim\GestureReloadAUGProne.rtm";
			leftHandIKCurve[] = {0,1,0.036,0,0.836,0,0.873,1};
		};
		class GestureReloadAUGContext: GestureReloadAUG
		{
			mask = "handsWeapon_context";
		};
		class GestureReloadAUGContextAnimDrive: GestureReloadAUG
		{
			mask = "handsWeapon_contextAnimDrive";
		};
		class GestureReloadSA80: GestureReloadBase
		{
			file = "\a3_aegis\weapons_f_aegis\data\anim\GestureReloadSA80.rtm";
			speed = 0.2;
			mask = "handsWeapon";
			headBobStrength = 0.25;
			headBobMode = 2;
			weaponIK = 1;
			leftHandIKCurve[] = {0,1,0.04,0,0.9,0,0.94,1};
		};
		class GestureReloadSA80Prone: GestureReloadSA80
		{
			file = "\a3_aegis\weapons_f_aegis\data\anim\GestureReloadSA80Prone.rtm";
			leftHandIKCurve[] = {0,1,0.04,0,0.9,0,0.94,1};
		};
		class GestureReloadSA80Context: GestureReloadSA80
		{
			mask = "handsWeapon_context";
		};
		class GestureReloadSA80ContextAnimDrive: GestureReloadSA80
		{
			mask = "handsWeapon_contextAnimDrive";
		};
		class GestureReloadG36: GestureReloadBase
		{
			file = "\a3_aegis\weapons_f_aegis\data\anim\GestureReloadG36.rtm";
			speed = 0.23;
			mask = "handsWeapon";
			headBobStrength = 0.25;
			headBobMode = 2;
			weaponIK = 1;
			leftHandIKCurve[] = {0,1,0.1,0,0.858,0,0.88,1};
		};
		class GestureReloadG36Prone: GestureReloadG36
		{
			file = "\a3_aegis\weapons_f_aegis\data\anim\GestureReloadG36Prone.rtm";
			leftHandIKCurve[] = {0,1,0.12,0,0.823,0,0.84,1};
		};
		class GestureReloadG36Context: GestureReloadG36
		{
			mask = "handsWeapon_context";
		};
		class GestureReloadG36ContextAnimDrive: GestureReloadG36
		{
			mask = "handsWeapon_contextAnimDrive";
		};
	};
};
class Mode_SemiAuto;
class Mode_Burst;
class Mode_FullAuto;
class asdg_MuzzleSlot;
class asdg_MuzzleSlot_65;
class asdg_MuzzleSlot_762R_PK;
class asdg_MuzzleSlot_556: asdg_MuzzleSlot{};
class asdg_MuzzleSlot_762: asdg_MuzzleSlot{};
class asdg_MuzzleSlot_762R_SVD: asdg_MuzzleSlot{};
class asdg_OpticRail;
class asdg_OpticRail1913: asdg_OpticRail
{
	class compatibleItems
	{
		aegis_acc_lrco_blk = 1;
		aegis_acc_lrco_sand = 1;
		optic_ico_01_black_f = 1;
		optic_ico_01_camo_f = 1;
		optic_ico_01_f = 1;
		optic_ico_01_sand_f = 1;
	};
};
class asdg_OpticRail1913_short;
class asdg_FrontSideRail;
class asdg_UnderSlot;
class CfgMagazines
{
	class CA_Magazine;
	class 30Rnd_545x39_Mag_Green_F;
	class aegis_30Rnd_545x39_7N10_6L23: 30Rnd_545x39_Mag_Green_F
	{
		author = "AveryTheKitty";
		picture = "\rhsafrf\addons\rhs_inventoryicons\data\magazines\rhs_30rnd_545x39_7n10_ak_ca.paa";
		displayName = "30rnd 6L23 Black (7N10)";
		displayNameShort = "7N10";
		descriptionShort = "Caliber: 5.45x39mm AP<br/>Rounds: 30<br/>Used in: AK-74, RPK-74";
		ammo = "rhs_B_545x39_7N10_Ball";
		initSpeed = 880;
		lastRoundsTracer = 0;
		hiddenSelections[] = {"camo"};
		hiddenSelectionsTextures[] = {"\a3_aegis\weapons_f_aegis\magazineproxies\data\magazine_ak74_black_co.paa"};
	};
	class aegis_30Rnd_545x39_7N22_6L23: 30Rnd_545x39_Mag_Green_F
	{
		author = "AveryTheKitty";
		picture = "\rhsafrf\addons\rhs_inventoryicons\data\magazines\rhs_30rnd_545x39_7n10_ak_ca.paa";
		displayName = "30rnd 6L23 Black (7N22)";
		displayNameShort = "7N22";
		descriptionShort = "Caliber: 5.45x39mm AP<br/>Rounds: 30<br/>Used in: AK-74, RPK-74";
		ammo = "rhs_B_545x39_7N22_Ball";
		initSpeed = 890;
		lastRoundsTracer = 0;
		hiddenSelections[] = {"camo"};
		hiddenSelectionsTextures[] = {"\a3_aegis\weapons_f_aegis\magazineproxies\data\magazine_ak74_black_co.paa"};
	};
	class aegis_30Rnd_545x39_7N10_6L23_arid: 30Rnd_545x39_Mag_Green_F
	{
		author = "AveryTheKitty";
		picture = "\rhsafrf\addons\rhs_inventoryicons\data\magazines\rhs_30rnd_545x39_7n10_ak_ca.paa";
		displayName = "30rnd 6L23 Arid (7N10)";
		displayNameShort = "7N10";
		descriptionShort = "Caliber: 5.45x39mm AP<br/>Rounds: 30<br/>Used in: AK-74, RPK-74";
		ammo = "rhs_B_545x39_7N10_Ball";
		initSpeed = 880;
		lastRoundsTracer = 0;
		hiddenSelections[] = {"camo"};
		hiddenSelectionsTextures[] = {"\a3_aegis\weapons_f_aegis\magazineproxies\data\magazine_ak74_camo_co.paa"};
	};
	class aegis_30Rnd_545x39_7N22_6L23_arid: 30Rnd_545x39_Mag_Green_F
	{
		author = "AveryTheKitty";
		picture = "\rhsafrf\addons\rhs_inventoryicons\data\magazines\rhs_30rnd_545x39_7n10_ak_ca.paa";
		displayName = "30rnd 6L23 Arid (7N22)";
		displayNameShort = "7N22";
		descriptionShort = "Caliber: 5.45x39mm AP<br/>Rounds: 30<br/>Used in: AK-74, RPK-74";
		ammo = "rhs_B_545x39_7N22_Ball";
		initSpeed = 890;
		lastRoundsTracer = 0;
		hiddenSelections[] = {"camo"};
		hiddenSelectionsTextures[] = {"\a3_aegis\weapons_f_aegis\magazineproxies\data\magazine_ak74_camo_co.paa"};
	};
	class aegis_30Rnd_545x39_7N10_6L23_lush: 30Rnd_545x39_Mag_Green_F
	{
		author = "AveryTheKitty";
		picture = "\rhsafrf\addons\rhs_inventoryicons\data\magazines\rhs_30rnd_545x39_7n10_ak_ca.paa";
		displayName = "30rnd 6L23 Lush (7N10)";
		displayNameShort = "7N10";
		descriptionShort = "Caliber: 5.45x39mm AP<br/>Rounds: 30<br/>Used in: AK-74, RPK-74";
		ammo = "rhs_B_545x39_7N10_Ball";
		initSpeed = 880;
		lastRoundsTracer = 0;
		hiddenSelections[] = {"camo"};
		hiddenSelectionsTextures[] = {"\a3_aegis\weapons_f_aegis\magazineproxies\data\magazine_ak74_khaki_co.paa"};
	};
	class aegis_30Rnd_545x39_7N22_6L23_lush: 30Rnd_545x39_Mag_Green_F
	{
		author = "AveryTheKitty";
		picture = "\rhsafrf\addons\rhs_inventoryicons\data\magazines\rhs_30rnd_545x39_7n10_ak_ca.paa";
		displayName = "30rnd 6L23 Lush (7N22)";
		displayNameShort = "7N22";
		descriptionShort = "Caliber: 5.45x39mm AP<br/>Rounds: 30<br/>Used in: AK-74, RPK-74";
		ammo = "rhs_B_545x39_7N22_Ball";
		initSpeed = 890;
		lastRoundsTracer = 0;
		hiddenSelections[] = {"camo"};
		hiddenSelectionsTextures[] = {"\a3_aegis\weapons_f_aegis\magazineproxies\data\magazine_ak74_khaki_co.paa"};
	};
	class 30Rnd_762x39_ak12_Mag_F;
	class 30rnd_762x39_ak12_arid_Mag_F;
	class 30rnd_762x39_ak12_lush_Mag_F;
	class aegis_30Rnd_545x39_7N10_ak12: 30Rnd_762x39_ak12_Mag_F
	{
		author = "AveryTheKitty";
		displayName = "30rnd AK-12 Black (7N10)";
		displayNameShort = "7N10";
		descriptionShort = "Caliber: 5.45x39mm AP<br/>Rounds: 30<br/>Used in: AK-74, RPK-74";
		ammo = "rhs_B_545x39_7N10_Ball";
		initSpeed = 880;
		lastRoundsTracer = 0;
	};
	class aegis_30Rnd_545x39_7N22_ak12: 30Rnd_762x39_ak12_Mag_F
	{
		author = "AveryTheKitty";
		displayName = "30rnd AK-12 Black (7N22)";
		displayNameShort = "7N22";
		descriptionShort = "Caliber: 5.45x39mm AP<br/>Rounds: 30<br/>Used in: AK-74, RPK-74";
		ammo = "rhs_B_545x39_7N22_Ball";
		initSpeed = 890;
		lastRoundsTracer = 0;
	};
	class aegis_30Rnd_545x39_7N10_ak12_arid: 30rnd_762x39_ak12_arid_Mag_F
	{
		author = "AveryTheKitty";
		displayName = "30rnd AK-12 Arid (7N10)";
		displayNameShort = "7N10";
		descriptionShort = "Caliber: 5.45x39mm AP<br/>Rounds: 30<br/>Used in: AK-74, RPK-74";
		ammo = "rhs_B_545x39_7N10_Ball";
		initSpeed = 880;
		lastRoundsTracer = 0;
	};
	class aegis_30Rnd_545x39_7N22_ak12_arid: 30rnd_762x39_ak12_arid_Mag_F
	{
		author = "AveryTheKitty";
		displayName = "30rnd AK-12 Arid (7N22)";
		displayNameShort = "7N22";
		descriptionShort = "Caliber: 5.45x39mm AP<br/>Rounds: 30<br/>Used in: AK-74, RPK-74";
		ammo = "rhs_B_545x39_7N22_Ball";
		initSpeed = 890;
		lastRoundsTracer = 0;
	};
	class aegis_30Rnd_545x39_7N10_ak12_lush: 30rnd_762x39_ak12_lush_Mag_F
	{
		author = "AveryTheKitty";
		displayName = "30rnd AK-12 Lush (7N10)";
		displayNameShort = "7N10";
		descriptionShort = "Caliber: 5.45x39mm AP<br/>Rounds: 30<br/>Used in: AK-74, RPK-74";
		ammo = "rhs_B_545x39_7N10_Ball";
		initSpeed = 880;
		lastRoundsTracer = 0;
	};
	class aegis_30Rnd_545x39_7N22_ak12_lush: 30rnd_762x39_ak12_lush_Mag_F
	{
		author = "AveryTheKitty";
		displayName = "30rnd AK-12 Lush (7N22)";
		displayNameShort = "7N22";
		descriptionShort = "Caliber: 5.45x39mm AP<br/>Rounds: 30<br/>Used in: AK-74, RPK-74";
		ammo = "rhs_B_545x39_7N22_Ball";
		initSpeed = 890;
		lastRoundsTracer = 0;
	};
	class 75rnd_762x39_ak12_Mag_F;
	class 75rnd_762x39_ak12_arid_Mag_F;
	class 75rnd_762x39_ak12_lush_Mag_F;
	class aegis_95Rnd_545x39_7N10_ak12: 75rnd_762x39_ak12_Mag_F
	{
		author = "AveryTheKitty";
		displayName = "95rnd AK-12 Black 7N10";
		displayNameShort = "7N10";
		descriptionShort = "Caliber: 5.45x39mm AP<br/>Rounds: 95<br/>Used in: AK-74, RPK-74";
		ammo = "rhs_B_545x39_7N10_Ball";
		mass = 36.4;
		count = 95;
		initSpeed = 880;
		lastRoundsTracer = 0;
		tracersEvery = 0;
	};
	class aegis_95Rnd_545x39_mixed_7N10_ak12: aegis_95Rnd_545x39_7N10_ak12
	{
		displayName = "95rnd AK-12 Black 7N10 (Mixed)";
		lastRoundsTracer = 5;
		tracersEvery = 5;
	};
	class aegis_95Rnd_545x39_7N22_ak12: 75rnd_762x39_ak12_Mag_F
	{
		author = "AveryTheKitty";
		displayName = "95rnd AK-12 Black 7N22";
		displayNameShort = "7N22";
		descriptionShort = "Caliber: 5.45x39mm AP<br/>Rounds: 95<br/>Used in: AK-74, RPK-74";
		ammo = "rhs_B_545x39_7N22_Ball";
		mass = 36.4;
		count = 95;
		initSpeed = 880;
		lastRoundsTracer = 0;
		tracersEvery = 0;
	};
	class aegis_95Rnd_545x39_mixed_7N22_ak12: aegis_95Rnd_545x39_7N22_ak12
	{
		displayName = "95rnd AK-12 Black 7N22 (Mixed)";
		lastRoundsTracer = 5;
		tracersEvery = 5;
	};
	class aegis_95Rnd_545x39_7N10_ak12_arid: 75rnd_762x39_ak12_arid_Mag_F
	{
		author = "AveryTheKitty";
		displayName = "95rnd AK-12 Arid 7N10";
		displayNameShort = "7N10";
		descriptionShort = "Caliber: 5.45x39mm AP<br/>Rounds: 95<br/>Used in: AK-74, RPK-74";
		ammo = "rhs_B_545x39_7N10_Ball";
		mass = 36.4;
		count = 95;
		initSpeed = 880;
		lastRoundsTracer = 0;
		tracersEvery = 0;
	};
	class aegis_95Rnd_545x39_mixed_7N10_ak12_arid: aegis_95Rnd_545x39_7N10_ak12_arid
	{
		displayName = "95rnd AK-12 Arid 7N10 (Mixed)";
		lastRoundsTracer = 5;
		tracersEvery = 5;
	};
	class aegis_95Rnd_545x39_7N22_ak12_arid: 75rnd_762x39_ak12_arid_Mag_F
	{
		author = "AveryTheKitty";
		displayName = "95rnd AK-12 Arid 7N22";
		displayNameShort = "7N22";
		descriptionShort = "Caliber: 5.45x39mm AP<br/>Rounds: 95<br/>Used in: AK-74, RPK-74";
		ammo = "rhs_B_545x39_7N22_Ball";
		mass = 36.4;
		count = 95;
		initSpeed = 880;
		lastRoundsTracer = 0;
		tracersEvery = 0;
	};
	class aegis_95Rnd_545x39_mixed_7N22_ak12_arid: aegis_95Rnd_545x39_7N22_ak12_arid
	{
		displayName = "95rnd AK-12 Arid 7N22 (Mixed)";
		lastRoundsTracer = 5;
		tracersEvery = 5;
	};
	class aegis_95Rnd_545x39_7N10_ak12_lush: 75rnd_762x39_ak12_lush_Mag_F
	{
		author = "AveryTheKitty";
		displayName = "95rnd AK-12 Lush 7N10";
		displayNameShort = "7N10";
		descriptionShort = "Caliber: 5.45x39mm AP<br/>Rounds: 95<br/>Used in: AK-74, RPK-74";
		ammo = "rhs_B_545x39_7N10_Ball";
		mass = 36.4;
		count = 95;
		initSpeed = 880;
		lastRoundsTracer = 0;
		tracersEvery = 0;
	};
	class aegis_95Rnd_545x39_mixed_7N10_ak12_lush: aegis_95Rnd_545x39_7N10_ak12_lush
	{
		displayName = "95rnd AK-12 Lush 7N10 (Mixed)";
		lastRoundsTracer = 5;
		tracersEvery = 5;
	};
	class aegis_95Rnd_545x39_7N22_ak12_lush: 75rnd_762x39_ak12_lush_Mag_F
	{
		author = "AveryTheKitty";
		displayName = "95rnd AK-12 Lush 7N22";
		displayNameShort = "7N22";
		descriptionShort = "Caliber: 5.45x39mm AP<br/>Rounds: 95<br/>Used in: AK-74, RPK-74";
		ammo = "rhs_B_545x39_7N22_Ball";
		mass = 36.4;
		count = 95;
		initSpeed = 880;
		lastRoundsTracer = 0;
		tracersEvery = 0;
	};
	class aegis_95Rnd_545x39_mixed_7N22_ak12_lush: aegis_95Rnd_545x39_7N22_ak12_lush
	{
		displayName = "95rnd AK-12 Lush 7N22 (Mixed)";
		lastRoundsTracer = 5;
		tracersEvery = 5;
	};
	class 30Rnd_556x45_Stanag;
	class aegis_30Rnd_556x45_aug: 30Rnd_556x45_Stanag
	{
		author = "AveryTheKitty";
		displayName = "30rnd AUG 5.56x45mm";
		descriptionShort = "Caliber: 5.56x45mm<br/>Rounds: 30<br/>Used in: AUR 90";
		modelspecial = "\a3_aegis\weapons_f_aegis\magazineproxies\data\mag_aug_30rnd";
		ammo = "B_556x45_Ball_Tracer_Red";
		hiddenSelections[] = {"Camo"};
		hiddenSelectionsTextures[] = {"\a3_aegis\weapons_f_aegis\rifles\aug\data\aug_co.paa"};
	};
	class aegis_30Rnd_556x45_aug_tracer_red: aegis_30Rnd_556x45_aug
	{
		displayName = "30rnd AUG 5.56x45mm Tracer (Red)";
		displayNameShort = "Tracer";
		tracersEvery = 1;
	};
};
class CfgMagazineWells
{
	class AK_545x39
	{
		aegisProxyMags[] = {"aegis_30Rnd_545x39_7N10_6L23","aegis_30Rnd_545x39_7N22_6L23","aegis_30Rnd_545x39_7N10_6L23_arid","aegis_30Rnd_545x39_7N22_6L23_arid","aegis_30Rnd_545x39_7N10_6L23_lush","aegis_30Rnd_545x39_7N22_6L23_lush","aegis_30Rnd_545x39_7N10_ak12","aegis_30Rnd_545x39_7N22_ak12","aegis_30Rnd_545x39_7N10_ak12_arid","aegis_30Rnd_545x39_7N22_ak12_arid","aegis_30Rnd_545x39_7N10_ak12_lush","aegis_30Rnd_545x39_7N22_ak12_lush","aegis_95Rnd_545x39_7N10_ak12","aegis_95Rnd_545x39_7N22_ak12","aegis_95Rnd_545x39_7N10_ak12_arid","aegis_95Rnd_545x39_7N22_ak12_arid","aegis_95Rnd_545x39_7N10_ak12_lush","aegis_95Rnd_545x39_7N22_ak12_lush","aegis_95Rnd_545x39_mixed_7N10_ak12","aegis_95Rnd_545x39_mixed_7N22_ak12","aegis_95Rnd_545x39_mixed_7N10_ak12_arid","aegis_95Rnd_545x39_mixed_7N22_ak12_arid","aegis_95Rnd_545x39_mixed_7N10_ak12_lush","aegis_95Rnd_545x39_mixed_7N22_ak12_lush"};
	};
	class CBA_545x39_RPK
	{
		aegisProxyMags[] = {"aegis_30Rnd_545x39_7N10_6L23","aegis_30Rnd_545x39_7N22_6L23","aegis_30Rnd_545x39_7N10_6L23_arid","aegis_30Rnd_545x39_7N22_6L23_arid","aegis_30Rnd_545x39_7N10_6L23_lush","aegis_30Rnd_545x39_7N22_6L23_lush","aegis_30Rnd_545x39_7N10_ak12","aegis_30Rnd_545x39_7N22_ak12","aegis_30Rnd_545x39_7N10_ak12_arid","aegis_30Rnd_545x39_7N22_ak12_arid","aegis_30Rnd_545x39_7N10_ak12_lush","aegis_30Rnd_545x39_7N22_ak12_lush","aegis_95Rnd_545x39_7N10_ak12","aegis_95Rnd_545x39_7N22_ak12","aegis_95Rnd_545x39_7N10_ak12_arid","aegis_95Rnd_545x39_7N22_ak12_arid","aegis_95Rnd_545x39_7N10_ak12_lush","aegis_95Rnd_545x39_7N22_ak12_lush","aegis_95Rnd_545x39_mixed_7N10_ak12","aegis_95Rnd_545x39_mixed_7N22_ak12","aegis_95Rnd_545x39_mixed_7N10_ak12_arid","aegis_95Rnd_545x39_mixed_7N22_ak12_arid","aegis_95Rnd_545x39_mixed_7N10_ak12_lush","aegis_95Rnd_545x39_mixed_7N22_ak12_lush"};
	};
	class CBA_556x45_STEYR
	{
		aegisProxyMags[] = {"aegis_30Rnd_556x45_aug","aegis_30Rnd_556x45_aug_tracer_red"};
	};
};
class CfgRecoils
{
	class recoil_default;
	class recoil_aegis_aug: recoil_default
	{
		muzzleOuter[] = {0.2,0.65,0.3,0.2};
		kickBack[] = {0.02,0.04};
		temporary = 0.01;
	};
	class recoil_aegis_sa80: recoil_default
	{
		muzzleOuter[] = {0.3,0.9,0.3,0.3};
		kickBack[] = {0.02,0.04};
		temporary = 0.01;
	};
	class recoil_aegis_g36: recoil_default
	{
		muzzleOuter[] = {0.3,0.8,0.35,0.25};
		kickBack[] = {0.02,0.04};
		temporary = 0.01;
	};
	class recoil_aegis_sdar: recoil_default
	{
		muzzleOuter[] = {0.3,0.7,0.3,0.3};
		kickBack[] = {0.02,0.04};
		temporary = 0.01;
	};
	class recoil_aegis_hk121: recoil_default
	{
		muzzleOuter[] = {0.7,1.2,0.35,0.25};
		kickBack[] = {0.03,0.05};
		temporary = 0.01;
	};
	class recoil_aegis_lwmmg: recoil_default
	{
		muzzleOuter[] = {0.7,1.1,0.3,0.35};
		kickBack[] = {0.02,0.04};
		temporary = 0.01;
	};
};
class CfgWeapons
{
	class Rifle;
	class Rifle_Base_F: Rifle
	{
		class GunParticles;
		class WeaponSlotsInfo;
	};
	class UGL_F;
	class aegis_aug_base: Rifle_Base_F
	{
		model = "\a3_aegis\weapons_f_aegis\rifles\aug";
		hiddenSelections[] = {"Camo"};
		hiddenSelectionsTextures[] = {"\a3_aegis\weapons_f_aegis\rifles\aug\data\aug_co.paa"};
		handAnim[] = {"OFP2_ManSkeleton","\a3_aegis\weapons_f_aegis\rifles\aug\data\anim\aug.rtm"};
		descriptionShort = "Assault Rifle";
		reloadAction = "GestureReloadAUG";
		magazines[] = {"aegis_30Rnd_556x45_aug","aegis_30Rnd_556x45_aug_tracer_red"};
		magazineWell[] = {"CBA_556x45_STEYR"};
		magazineReloadSwitchPhase = 0.48;
		htMin = 9;
		htMax = 870;
		inertia = 0.4;
		aimTransitionSpeed = 1.1;
		dexterity = 1.6;
		initSpeed = 970;
		recoil = "recoil_aegis_aug";
		maxZeroing = 1000;
		UiPicture = "\A3\Weapons_F\Data\UI\icon_regular_CA.paa";
		class WeaponSlotsInfo: WeaponSlotsInfo
		{
			class MuzzleSlot: asdg_MuzzleSlot_556
			{
				iconPosition[] = {0,0.38};
				iconScale = 0.2;
			};
			class CowsSlot: asdg_OpticRail1913
			{
				iconPosition[] = {0.479,0.2};
				iconScale = 0.2;
			};
			class PointerSlot: asdg_FrontSideRail
			{
				iconPosition[] = {0.285,0.35};
				iconScale = 0.2;
			};
			mass = 80;
		};
		modes[] = {"Single","FullAuto","AI_Close","AI_Medium","AI_Far"};
		class Single: Mode_SemiAuto
		{
			reloadTime = 0.088;
			dispersion = 0.000872665;
			minRange = 0;
			minRangeProbab = 0;
			midRange = 0;
			midRangeProbab = 0;
			maxRange = 0;
			maxRangeProbab = 0;
			class BaseSoundModeType;
			class StandardSound: BaseSoundModeType
			{
				soundSetShot[] = {"jsrs_type115_shot_soundset","jsrs_6x5mm_reverb_soundset"};
			};
			class SilencedSound: BaseSoundModeType
			{
				soundSetShot[] = {"jsrs_mx_shot_silenced_soundset","jsrs_6x5mm_sd_reverb_soundset"};
			};
		};
		class FullAuto: Mode_FullAuto
		{
			reloadTime = 0.088;
			dispersion = 0.000872665;
			minRange = 0;
			minRangeProbab = 0;
			midRange = 0;
			midRangeProbab = 0;
			maxRange = 0;
			maxRangeProbab = 0;
			class BaseSoundModeType;
			class StandardSound: BaseSoundModeType
			{
				soundSetShot[] = {"jsrs_type115_shot_soundset","jsrs_6x5mm_reverb_soundset"};
			};
			class SilencedSound: BaseSoundModeType
			{
				soundSetShot[] = {"jsrs_mx_shot_silenced_soundset","jsrs_6x5mm_sd_reverb_soundset"};
			};
		};
		class AI_Close: Single
		{
			showToPlayer = 0;
			burstRangeMax = 4;
			minRange = 2;
			minRangeProbab = 0.5;
			midRange = 100;
			midRangeProbab = 0.8;
			maxRange = 300;
			maxRangeProbab = 0.2;
			aiRateOfFire = 1;
			aiRateOfFireDispersion = 1.5;
			aiRateOfFireDistance = 100;
		};
		class AI_Medium: AI_Close
		{
			burstRangeMax = 3;
			minRange = 200;
			minRangeProbab = 0.2;
			midRange = 400;
			midRangeProbab = 0.7;
			maxRange = 600;
			maxRangeProbab = 0.1;
			aiRateOfFire = 1;
			aiRateOfFireDispersion = 2;
			aiRateOfFireDistance = 400;
		};
		class AI_Far: AI_Close
		{
			burstRangeMax = 3;
			minRange = 600;
			minRangeProbab = 0.2;
			midRange = 800;
			midRangeProbab = 0.7;
			maxRange = 1000;
			maxRangeProbab = 0.1;
			aiRateOfFire = 1;
			aiRateOfFireDispersion = 3;
			aiRateOfFireDistance = 800;
		};
		bullet1[] = {"\A3\Sounds_F\weapons\shells\7_62\metal_762_01","db-6",1,15};
		bullet2[] = {"\A3\Sounds_F\weapons\shells\7_62\metal_762_02","db-6",1,15};
		bullet3[] = {"\A3\Sounds_F\weapons\shells\7_62\metal_762_03","db-6",1,15};
		bullet4[] = {"\A3\Sounds_F\weapons\shells\7_62\metal_762_04","db-6",1,15};
		bullet5[] = {"\A3\Sounds_F\weapons\shells\7_62\dirt_762_01","db-8",1,15};
		bullet6[] = {"\A3\Sounds_F\weapons\shells\7_62\dirt_762_02","db-8",1,15};
		bullet7[] = {"\A3\Sounds_F\weapons\shells\7_62\dirt_762_03","db-8",1,15};
		bullet8[] = {"\A3\Sounds_F\weapons\shells\7_62\dirt_762_04","db-8",1,15};
		bullet9[] = {"\A3\Sounds_F\weapons\shells\7_62\grass_762_01","db-12",1,15};
		bullet10[] = {"\A3\Sounds_F\weapons\shells\7_62\grass_762_02","db-12",1,15};
		bullet11[] = {"\A3\Sounds_F\weapons\shells\7_62\grass_762_03","db-12",1,15};
		bullet12[] = {"\A3\Sounds_F\weapons\shells\7_62\grass_762_04","db-12",1,15};
		soundBullet[] = {"bullet1","1/12","bullet2","1/12","bullet3","1/12","bullet4","1/12","bullet5","1/12","bullet6","1/12","bullet7","1/12","bullet8","1/12","bullet9","1/12","bullet10","1/12","bullet11","1/12","bullet12","1/12"};
		drySound[] = {"\a3_aegis\weapons_f_aegis\rifles\aug\data\sound\aug_dry","db-2",1,10};
		reloadMagazineSound[] = {"\a3_aegis\weapons_f_aegis\rifles\aug\data\sound\aug_reload","db0",1,10};
		changeFiremodeSound[] = {"\a3_aegis\weapons_f_aegis\rifles\aug\data\sound\aug_firemode","db-10",1,5};
	};
	class aegis_aug_gl_base: aegis_aug_base
	{
		model = "\a3_aegis\weapons_f_aegis\rifles\aug_gl";
		hiddenSelections[] = {"Camo1","Camo2"};
		hiddenSelectionsTextures[] = {"\a3_aegis\weapons_f_aegis\rifles\aug\data\aug_co.paa","\a3_aegis\weapons_f_aegis\rifles\aug\data\gl40_co.paa"};
		handAnim[] = {"OFP2_ManSkeleton","\a3_aegis\weapons_f_aegis\rifles\aug\data\anim\aug_gl.rtm"};
		inertia = 0.5;
		dexterity = 1.6;
		aimTransitionSpeed = 0.95;
		UiPicture = "\a3\weapons_f\data\ui\icon_gl_ca.paa";
		class WeaponSlotsInfo: WeaponSlotsInfo
		{
			mass = 100;
		};
		class EGLM: UGL_F
		{
			displayName = "EGLM-40";
			useModelOptics = 0;
			useExternalOptic = 0;
			cameraDir = "OP_look";
			discreteDistance[] = {50,75,100,150,200,250,300,350,400};
			discreteDistanceCameraPoint[] = {"OP_eye_50","OP_eye_75","OP_eye_100","OP_eye_150","OP_eye_200","OP_eye_250","OP_eye_300","OP_eye_350","OP_eye_400"};
			discreteDistanceInitIndex = 1;
			reloadAction = "GestureReloadKatibaUGL";
			reloadMagazineSound[] = {"\a3_aegis\weapons_f_aegis\rifles\aug\data\sound\aug_ugl_reload","db-2",1,10};
		};
		muzzles[] = {"this","EGLM"};
	};
	class aegis_aug_carbine_base: aegis_aug_base
	{
		model = "\a3_aegis\weapons_f_aegis\rifles\aug_c";
		inertia = 0.3;
		dexterity = 1.6;
		aimTransitionSpeed = 1.2;
		class WeaponSlotsInfo: WeaponSlotsInfo
		{
			mass = 65;
		};
	};
	class aegis_weap_aur90: aegis_aug_base
	{
		scope = 2;
		author = "AveryTheKitty";
		displayName = "AUR-90 (Black)";
		picture = "\a3_aegis\weapons_f_aegis\rifles\aug\data\ui\icon_arifle_aug_black_f_x_ca.paa";
		baseWeapon = "aegis_weap_aur90";
	};
	class aegis_weap_aur90_tan: aegis_weap_aur90
	{
		displayName = "AUR-90 (Tan)";
		picture = "\a3_aegis\weapons_f_aegis\rifles\aug\data\ui\icon_arifle_aug_tan_f_x_ca.paa";
		baseWeapon = "aegis_weap_aur90_tan";
		hiddenSelectionsTextures[] = {"\a3_aegis\weapons_f_aegis\rifles\aug\data\aug_tan_co.paa"};
	};
	class aegis_weap_aur90_eglm: aegis_aug_gl_base
	{
		scope = 2;
		author = "AveryTheKitty";
		displayName = "AUR-90 EGLM (Black)";
		picture = "\a3_aegis\weapons_f_aegis\rifles\aug\data\ui\icon_arifle_aug_gl_black_f_x_ca.paa";
		baseWeapon = "aegis_weap_aur90_eglm";
	};
	class aegis_weap_aur90_eglm_tan: aegis_weap_aur90_eglm
	{
		displayName = "AUR-90 EGLM (Tan)";
		picture = "\a3_aegis\weapons_f_aegis\rifles\aug\data\ui\icon_arifle_aug_gl_tan_f_x_ca.paa";
		baseWeapon = "aegis_weap_aur90_eglm_tan";
		hiddenSelectionsTextures[] = {"\a3_aegis\weapons_f_aegis\rifles\aug\data\aug_tan_co.paa","\a3_aegis\weapons_f_aegis\rifles\aug\data\gl40_co.paa"};
	};
	class aegis_weap_aur90_carbine: aegis_aug_carbine_base
	{
		scope = 2;
		author = "AveryTheKitty";
		displayName = "AUR-90C (Black)";
		picture = "\a3_aegis\weapons_f_aegis\rifles\aug\data\ui\icon_arifle_aug_c_black_f_x_ca.paa";
		baseWeapon = "aegis_weap_aur90_carbine";
	};
	class aegis_weap_aur90_carbine_tan: aegis_weap_aur90_carbine
	{
		displayName = "AUR-90C (Tan)";
		picture = "\a3_aegis\weapons_f_aegis\rifles\aug\data\ui\icon_arifle_aug_c_tan_f_x_ca.paa";
		baseWeapon = "aegis_weap_aur90_carbine_tan";
		hiddenSelectionsTextures[] = {"\a3_aegis\weapons_f_aegis\rifles\aug\data\aug_tan_co.paa"};
	};
	class aegis_sa80_base: Rifle_Base_F
	{
		model = "\a3_aegis\weapons_f_aegis\rifles\sa80";
		hiddenSelections[] = {"camo1","camo2","camo3"};
		descriptionShort = "Assault Rifle";
		handAnim[] = {"OFP2_ManSkeleton","\a3_aegis\weapons_f_aegis\rifles\sa80\data\anim\sa80_vfg.rtm"};
		reloadAction = "GestureReloadSA80";
		magazines[] = {"30Rnd_65x39_caseless_black_mag"};
		magazineWell[] = {"MX_65x39"};
		magazineReloadSwitchPhase = 0.34;
		recoil = "recoil_aegis_sa80";
		initSpeed = 930;
		inertia = 0.5;
		dexterity = 1.6;
		aimTransitionSpeed = 1;
		maxZeroing = 1000;
		discreteDistance[] = {100,200,300,400,500,600};
		discreteDistanceInitIndex = 1;
		class WeaponSlotsInfo: WeaponSlotsInfo
		{
			class MuzzleSlot: asdg_MuzzleSlot_65
			{
				iconPosition[] = {0.043,0.35};
				iconScale = 0.2;
			};
			class CowsSlot: asdg_OpticRail1913
			{
				iconPosition[] = {0.48,0.195};
				iconScale = 0.2;
			};
			class PointerSlot: asdg_FrontSideRail
			{
				iconPosition[] = {0.285,0.35};
				iconScale = 0.2;
			};
			class UnderBarrelSlot{};
			mass = 80;
		};
		modes[] = {"Single","FullAuto","AI_Close","AI_Medium","AI_Far"};
		class Single: Mode_SemiAuto
		{
			reloadTime = 0.088;
			dispersion = 0.000872665;
			minRange = 0;
			minRangeProbab = 0;
			midRange = 0;
			midRangeProbab = 0;
			maxRange = 0;
			maxRangeProbab = 0;
			class BaseSoundModeType;
			class StandardSound: BaseSoundModeType
			{
				soundSetShot[] = {"jsrs_type115_shot_soundset","jsrs_6x5mm_reverb_soundset"};
			};
			class SilencedSound: BaseSoundModeType
			{
				soundSetShot[] = {"jsrs_mx_shot_silenced_soundset","jsrs_6x5mm_sd_reverb_soundset"};
			};
		};
		class FullAuto: Mode_FullAuto
		{
			reloadTime = 0.088;
			dispersion = 0.000872665;
			minRange = 0;
			minRangeProbab = 0;
			midRange = 0;
			midRangeProbab = 0;
			maxRange = 0;
			maxRangeProbab = 0;
			class BaseSoundModeType;
			class StandardSound: BaseSoundModeType
			{
				soundSetShot[] = {"jsrs_type115_shot_soundset","jsrs_6x5mm_reverb_soundset"};
			};
			class SilencedSound: BaseSoundModeType
			{
				soundSetShot[] = {"jsrs_mx_shot_silenced_soundset","jsrs_6x5mm_sd_reverb_soundset"};
			};
		};
		class AI_Close: Single
		{
			showToPlayer = 0;
			burstRangeMax = 4;
			minRange = 2;
			minRangeProbab = 0.5;
			midRange = 100;
			midRangeProbab = 0.8;
			maxRange = 300;
			maxRangeProbab = 0.2;
			aiRateOfFire = 1;
			aiRateOfFireDispersion = 1.5;
			aiRateOfFireDistance = 100;
		};
		class AI_Medium: AI_Close
		{
			burstRangeMax = 3;
			minRange = 200;
			minRangeProbab = 0.2;
			midRange = 400;
			midRangeProbab = 0.7;
			maxRange = 600;
			maxRangeProbab = 0.1;
			aiRateOfFire = 1;
			aiRateOfFireDispersion = 2;
			aiRateOfFireDistance = 400;
		};
		class AI_Far: AI_Close
		{
			burstRangeMax = 3;
			minRange = 600;
			minRangeProbab = 0.2;
			midRange = 800;
			midRangeProbab = 0.7;
			maxRange = 1000;
			maxRangeProbab = 0.1;
			aiRateOfFire = 1;
			aiRateOfFireDispersion = 3;
			aiRateOfFireDistance = 800;
		};
		deployedPivot = "bipod";
		hasBipod = 1;
		class GunParticles: GunParticles
		{
			class SecondEffect
			{
				positionName = "Nabojnicestart";
				directionName = "Nabojniceend";
				effectName = "CaselessAmmoCloud";
			};
		};
		soundBipodDown[] = {"\a3\sounds_f_mark\arsenal\sfx\bipods\bipod_generic_down","db-3",1,20};
		soundBipodUp[] = {"\a3\sounds_f_mark\arsenal\sfx\bipods\bipod_generic_up","db-3",1,20};
		drySound[] = {"\a3_aegis\weapons_f_aegis\rifles\sa80\data\sound\l85a3_dry","db-2",1,10};
		reloadMagazineSound[] = {"\a3_aegis\weapons_f_aegis\rifles\sa80\data\sound\l85a3_reload","db10",1,10};
		changeFiremodeSound[] = {"\a3_aegis\weapons_f_aegis\rifles\sa80\data\sound\l85a3_firemode","db-5",1,5};
		ACE_barrelTwist = 180.5;
		ACE_barrelLength = 518;
	};
	class aegis_sa80_gl_base: aegis_sa80_base
	{
		model = "\a3_aegis\weapons_f_aegis\rifles\sa80_gl";
		handAnim[] = {"OFP2_ManSkeleton","\a3_aegis\weapons_f_aegis\rifles\sa80\data\anim\sa80_gl.rtm"};
		inertia = 0.6;
		aimTransitionSpeed = 0.95;
		uiPicture = "\a3\weapons_f\data\ui\icon_gl_ca.paa";
		class WeaponSlotsInfo: WeaponSlotsInfo
		{
			class UnderBarrelSlot: asdg_UnderSlot
			{
				iconPosition[] = {0.123,0.789};
				iconScale = 0.2;
			};
			mass = 94;
		};
		muzzles[] = {"this","EGLM"};
		class EGLM: UGL_F
		{
			displayName = "EGLM-40";
			useModelOptics = 0;
			useExternalOptic = 0;
			cameraDir = "OP_look";
			discreteDistance[] = {50,75,100,150,200,250,300,350,400};
			discreteDistanceCameraPoint[] = {"OP_eye_50","OP_eye_75","OP_eye_100","OP_eye_150","OP_eye_200","OP_eye_250","OP_eye_300","OP_eye_350","OP_eye_400"};
			discreteDistanceInitIndex = 1;
			reloadAction = "GestureReloadSPARUGL";
			magazineReloadSwitchPhase = 0.4;
			reloadMagazineSound[] = {"\a3_aegis\weapons_f_aegis\rifles\sa80\data\sound\l85a3_ugl_reload","db-2",1,10};
		};
		hasBipod = 0;
	};
	class aegis_sa80_carbine_base: aegis_sa80_base
	{
		model = "\a3_aegis\weapons_f_aegis\rifles\sa80c";
		handAnim[] = {"OFP2_ManSkeleton","\a3_aegis\weapons_f_aegis\rifles\sa80\data\anim\sa80_c.rtm"};
		initSpeed = 780;
		inertia = 0.4;
		dexterity = 1.7;
		aimTransitionSpeed = 1.2;
		maxZeroing = 600;
		class WeaponSlotsInfo: WeaponSlotsInfo
		{
			class CowsSlot: asdg_OpticRail1913_short{};
			class MuzzleSlot: asdg_MuzzleSlot_65
			{
				iconPosition[] = {0.043,0.348};
				iconScale = 0.2;
			};
			class PointerSlot: asdg_FrontSideRail
			{
				iconPosition[] = {0.285,0.344};
				iconScale = 0.2;
			};
			mass = 65;
		};
		class Single: Single
		{
			dispersion = 0.00116355;
		};
		class FullAuto: FullAuto
		{
			dispersion = 0.00116355;
		};
		hasBipod = 0;
		ACE_barrelLength = 285;
	};
	class aegis_weap_sa80_blk: aegis_sa80_base
	{
		scope = 2;
		author = "AveryTheKitty";
		displayName = "L85A3 6.5x39mm (Black)";
		picture = "\a3_aegis\weapons_f_aegis\rifles\sa80\data\ui\icon_arifle_sa80_blk_f_x_ca.paa";
		baseWeapon = "aegis_weap_sa80_blk";
		hiddenSelectionsTextures[] = {"\a3_aegis\weapons_f_aegis\rifles\sa80\data\sa80_f_01_co.paa","\a3_aegis\weapons_f_aegis\rifles\sa80\data\sa80_f_02_co.paa","\a3_aegis\weapons_f_aegis\rifles\sa80\data\grip_co.paa"};
	};
	class aegis_weap_sa80_eglm_blk: aegis_sa80_gl_base
	{
		scope = 2;
		author = "AveryTheKitty";
		displayName = "L85A3 6.5x39mm EGLM (Black)";
		picture = "\a3_aegis\weapons_f_aegis\rifles\sa80\data\ui\icon_arifle_sa80_gl_blk_f_x_ca.paa";
		baseWeapon = "aegis_weap_sa80_eglm_blk";
		hiddenSelectionsTextures[] = {"\a3_aegis\weapons_f_aegis\rifles\sa80\data\sa80_f_01_co.paa","\a3_aegis\weapons_f_aegis\rifles\sa80\data\sa80_f_02_co.paa","\a3_aegis\weapons_f_aegis\rifles\sa80\data\sa80_f_gl_co.paa"};
	};
	class aegis_weap_sa80c_blk: aegis_sa80_carbine_base
	{
		scope = 2;
		author = "AveryTheKitty";
		displayName = "L85A3 6.5x39mm Carbine (Black)";
		picture = "\a3_aegis\weapons_f_aegis\rifles\sa80\data\ui\icon_arifle_sa80_c_blk_f_x_ca.paa";
		baseWeapon = "aegis_weap_sa80c_blk";
		hiddenSelectionsTextures[] = {"\a3_aegis\weapons_f_aegis\rifles\sa80\data\sa80_f_01_co.paa","\a3_aegis\weapons_f_aegis\rifles\sa80\data\sa80_f_c_co.paa"};
	};
	class aegis_weap_sa80_khk: aegis_sa80_base
	{
		scope = 2;
		author = "AveryTheKitty";
		displayName = "L85A3 6.5x39mm (Khaki)";
		picture = "\a3_aegis\weapons_f_aegis\rifles\sa80\data\ui\icon_arifle_sa80_khk_f_x_ca.paa";
		baseWeapon = "aegis_weap_sa80_khk";
		hiddenSelectionsTextures[] = {"\a3_aegis\weapons_f_aegis\rifles\sa80\data\sa80_f_01_khk_co.paa","\a3_aegis\weapons_f_aegis\rifles\sa80\data\sa80_f_02_khk_co.paa","\a3_aegis\weapons_f_aegis\rifles\sa80\data\grip_co.paa"};
	};
	class aegis_weap_sa80_eglm_khk: aegis_sa80_gl_base
	{
		scope = 2;
		author = "AveryTheKitty";
		displayName = "L85A3 6.5x39mm EGLM (Khaki)";
		picture = "\a3_aegis\weapons_f_aegis\rifles\sa80\data\ui\icon_arifle_sa80_gl_khk_f_x_ca.paa";
		baseWeapon = "aegis_weap_sa80_eglm_khk";
		hiddenSelectionsTextures[] = {"\a3_aegis\weapons_f_aegis\rifles\sa80\data\sa80_f_01_khk_co.paa","\a3_aegis\weapons_f_aegis\rifles\sa80\data\sa80_f_02_khk_co.paa","\a3_aegis\weapons_f_aegis\rifles\sa80\data\sa80_f_gl_khk_co.paa"};
	};
	class aegis_weap_sa80c_khk: aegis_sa80_carbine_base
	{
		scope = 2;
		author = "AveryTheKitty";
		displayName = "L85A3 6.5x39mm Carbine (Khaki)";
		picture = "\a3_aegis\weapons_f_aegis\rifles\sa80\data\ui\icon_arifle_sa80_c_khk_f_x_ca.paa";
		baseWeapon = "aegis_weap_sa80c_khk";
		hiddenSelectionsTextures[] = {"\a3_aegis\weapons_f_aegis\rifles\sa80\data\sa80_f_01_khk_co.paa","\a3_aegis\weapons_f_aegis\rifles\sa80\data\sa80_f_c_khk_co.paa"};
	};
	class aegis_weap_sa80_sand: aegis_sa80_base
	{
		scope = 2;
		author = "AveryTheKitty";
		displayName = "L85A3 6.5x39mm (Sand)";
		picture = "\a3_aegis\weapons_f_aegis\rifles\sa80\data\ui\icon_arifle_sa80_snd_f_x_ca.paa";
		baseWeapon = "aegis_weap_sa80_sand";
		hiddenSelectionsTextures[] = {"\a3_aegis\weapons_f_aegis\rifles\sa80\data\sa80_f_01_snd_co.paa","\a3_aegis\weapons_f_aegis\rifles\sa80\data\sa80_f_02_snd_co.paa","\a3_aegis\weapons_f_aegis\rifles\sa80\data\grip_co.paa"};
	};
	class aegis_weap_sa80_eglm_sand: aegis_sa80_gl_base
	{
		scope = 2;
		author = "AveryTheKitty";
		displayName = "L85A3 6.5x39mm EGLM (Sand)";
		picture = "\a3_aegis\weapons_f_aegis\rifles\sa80\data\ui\icon_arifle_sa80_gl_snd_f_x_ca.paa";
		baseWeapon = "aegis_weap_sa80_eglm_sand";
		hiddenSelectionsTextures[] = {"\a3_aegis\weapons_f_aegis\rifles\sa80\data\sa80_f_01_snd_co.paa","\a3_aegis\weapons_f_aegis\rifles\sa80\data\sa80_f_02_snd_co.paa","\a3_aegis\weapons_f_aegis\rifles\sa80\data\sa80_f_gl_snd_co.paa"};
	};
	class aegis_weap_sa80c_sand: aegis_sa80_carbine_base
	{
		scope = 2;
		author = "AveryTheKitty";
		displayName = "L85A3 6.5x39mm Carbine (Sand)";
		picture = "\a3_aegis\weapons_f_aegis\rifles\sa80\data\ui\icon_arifle_sa80_c_snd_f_x_ca.paa";
		baseWeapon = "aegis_weap_sa80c_sand";
		hiddenSelectionsTextures[] = {"\a3_aegis\weapons_f_aegis\rifles\sa80\data\sa80_f_01_snd_co.paa","\a3_aegis\weapons_f_aegis\rifles\sa80\data\sa80_f_c_snd_co.paa"};
	};
	class aegis_g36_base: Rifle_Base_F
	{
		picture = "\a3_aegis\weapons_f_aegis\rifles\g36\data\ui\icon_arifle_g36_f_x_ca.paa";
		model = "\a3_aegis\weapons_f_aegis\rifles\g36";
		hiddenSelections[] = {"camo1","camo2"};
		hiddenSelectionsTextures[] = {"\a3_aegis\weapons_f_aegis\rifles\g36\data\g36_f_01_co.paa","\a3_aegis\weapons_f_aegis\rifles\g36\data\g36_f_02_co.paa"};
		descriptionShort = "Assault Rifle";
		handAnim[] = {"OFP2_ManSkeleton","\a3\weapons_f_exp\rifles\spar_02\data\anim\spar_02.rtm"};
		reloadAction = "GestureReloadG36";
		magazines[] = {"30Rnd_65x39_caseless_msbs_mag","30Rnd_65x39_caseless_msbs_mag_Tracer"};
		magazineWell[] = {"MX_65x39_MSBS"};
		magazineReloadSwitchPhase = 0.48;
		recoil = "recoil_aegis_g36";
		initSpeed = 850;
		inertia = 0.5;
		dexterity = 1.6;
		aimTransitionSpeed = 1.2;
		maxZeroing = 800;
		discreteDistance[] = {100,200,300,400,500,600};
		discreteDistanceInitIndex = 1;
		class WeaponSlotsInfo: WeaponSlotsInfo
		{
			class MuzzleSlot: asdg_MuzzleSlot_65
			{
				iconPosition[] = {0,0.38};
				iconScale = 0.2;
			};
			class CowsSlot: asdg_OpticRail1913
			{
				iconPosition[] = {0.479,0.194};
				iconScale = 0.2;
			};
			class PointerSlot: asdg_FrontSideRail
			{
				iconPosition[] = {0.285,0.34};
				iconScale = 0.2;
			};
			class UnderBarrelSlot: asdg_UnderSlot
			{
				iconPosition[] = {0.285,0.34};
				iconScale = 0.2;
			};
			mass = 84;
		};
		modes[] = {"Single","FullAuto","AI_Close","AI_Medium","AI_Far"};
		class Single: Mode_SemiAuto
		{
			reloadTime = 0.08;
			dispersion = 0.000872665;
			minRange = 0;
			minRangeProbab = 0;
			midRange = 0;
			midRangeProbab = 0;
			maxRange = 0;
			maxRangeProbab = 0;
			class BaseSoundModeType;
			class StandardSound: BaseSoundModeType
			{
				soundSetShot[] = {"jsrs_type115_shot_soundset","jsrs_6x5mm_reverb_soundset"};
			};
			class SilencedSound: BaseSoundModeType
			{
				soundSetShot[] = {"jsrs_mx_shot_silenced_soundset","jsrs_6x5mm_sd_reverb_soundset"};
			};
		};
		class FullAuto: Mode_FullAuto
		{
			reloadTime = 0.08;
			dispersion = 0.000872665;
			minRange = 0;
			minRangeProbab = 0;
			midRange = 0;
			midRangeProbab = 0;
			maxRange = 0;
			maxRangeProbab = 0;
			class BaseSoundModeType;
			class StandardSound: BaseSoundModeType
			{
				soundSetShot[] = {"jsrs_type115_shot_soundset","jsrs_6x5mm_reverb_soundset"};
			};
			class SilencedSound: BaseSoundModeType
			{
				soundSetShot[] = {"jsrs_mx_shot_silenced_soundset","jsrs_6x5mm_sd_reverb_soundset"};
			};
		};
		class AI_Close: Single
		{
			showToPlayer = 0;
			burstRangeMax = 4;
			minRange = 2;
			minRangeProbab = 0.5;
			midRange = 100;
			midRangeProbab = 0.8;
			maxRange = 300;
			maxRangeProbab = 0.2;
			aiRateOfFire = 1;
			aiRateOfFireDispersion = 1.5;
			aiRateOfFireDistance = 100;
		};
		class AI_Medium: AI_Close
		{
			burstRangeMax = 3;
			minRange = 200;
			minRangeProbab = 0.2;
			midRange = 400;
			midRangeProbab = 0.7;
			maxRange = 600;
			maxRangeProbab = 0.1;
			aiRateOfFire = 1;
			aiRateOfFireDispersion = 2;
			aiRateOfFireDistance = 400;
		};
		class AI_Far: AI_Close
		{
			burstRangeMax = 3;
			minRange = 600;
			minRangeProbab = 0.2;
			midRange = 800;
			midRangeProbab = 0.7;
			maxRange = 1000;
			maxRangeProbab = 0.1;
			aiRateOfFire = 1;
			aiRateOfFireDispersion = 3;
			aiRateOfFireDistance = 800;
		};
		class GunParticles: GunParticles
		{
			class SecondEffect
			{
				positionName = "Nabojnicestart";
				directionName = "Nabojniceend";
				effectName = "CaselessAmmoCloud";
			};
		};
		drySound[] = {"\a3_aegis\weapons_f_aegis\rifles\g36\data\sound\g36_dry","db-2",1,10};
		reloadMagazineSound[] = {"\a3_aegis\weapons_f_aegis\rifles\g36\data\sound\g36_reload","db0",1,10};
		changeFiremodeSound[] = {"\a3_aegis\weapons_f_aegis\rifles\g36\data\sound\g36_firemode","db-2",1,5};
	};
	class aegis_g36_gl_base: aegis_g36_base
	{
		picture = "\a3_aegis\weapons_f_aegis\rifles\g36\data\ui\icon_arifle_g36_gl_f_x_ca.paa";
		model = "\a3_aegis\weapons_f_aegis\rifles\g36_gl";
		hiddenSelections[] = {"camo1","camo2","camo3"};
		hiddenSelectionsTextures[] = {"\a3_aegis\weapons_f_aegis\rifles\g36\data\g36_f_01_co.paa","\a3_aegis\weapons_f_aegis\rifles\g36\data\g36_f_02_co.paa","\a3_aegis\weapons_f_aegis\rifles\g36\data\g36_f_gl_co.paa"};
		uiPicture = "\a3\weapons_f\data\ui\icon_gl_ca.paa";
		handAnim[] = {"OFP2_ManSkeleton","\a3\weapons_f_exp\rifles\spar_01\data\anim\spar_01_gl.rtm"};
		inertia = 0.6;
		aimTransitionSpeed = 1;
		class WeaponSlotsInfo: WeaponSlotsInfo
		{
			class UnderBarrelSlot: asdg_UnderSlot
			{
				iconPosition[] = {0.285,0.344};
				iconScale = 0.2;
			};
			mass = 98;
		};
		muzzles[] = {"this","UGL"};
		class UGL: UGL_F
		{
			displayName = "EGLM-40";
			useModelOptics = 0;
			useExternalOptic = 0;
			cameraDir = "OP_look";
			discreteDistance[] = {50,75,100,150,200,250,300,350,400};
			discreteDistanceCameraPoint[] = {"OP_eye_50","OP_eye_75","OP_eye_100","OP_eye_150","OP_eye_200","OP_eye_250","OP_eye_300","OP_eye_350","OP_eye_400"};
			discreteDistanceInitIndex = 1;
			reloadAction = "GestureReloadSPARUGL";
			magazineReloadSwitchPhase = 0.4;
			reloadMagazineSound[] = {"\a3_aegis\weapons_f_aegis\rifles\g36c\data\sound\g36_ugl_reload","db-2",1,10};
		};
	};
	class aegis_g36c_base: aegis_g36_base
	{
		picture = "\a3_aegis\weapons_f_aegis\rifles\g36\data\ui\icon_arifle_g36c_f_x_ca.paa";
		model = "\a3_aegis\weapons_f_aegis\rifles\g36c";
		handAnim[] = {"OFP2_ManSkeleton","\a3\weapons_f_exp\rifles\spar_02\data\anim\spar_02.rtm"};
		initSpeed = 722;
		inertia = 0.4;
		dexterity = 1.7;
		aimTransitionSpeed = 1.3;
		maxZeroing = 600;
		class WeaponSlotsInfo: WeaponSlotsInfo
		{
			class UnderBarrelSlot: asdg_UnderSlot
			{
				iconPosition[] = {0.285,0.344};
				iconScale = 0.2;
			};
			mass = 70;
		};
		class Single: Single
		{
			dispersion = 0.00116355;
		};
		class FullAuto: FullAuto
		{
			dispersion = 0.00116355;
		};
	};
	class aegis_weap_g36k_65_blk: aegis_g36_base
	{
		scope = 2;
		author = "AveryTheKitty, Toadie2K";
		displayName = "G36K 6.5mm (Black)";
		baseWeapon = "aegis_weap_g36k_65_blk";
	};
	class aegis_weap_g36k_gl_65_blk: aegis_g36_gl_base
	{
		scope = 2;
		author = "AveryTheKitty, Toadie2K";
		displayName = "G36K 6.5mm GL (Black)";
		baseWeapon = "aegis_weap_g36k_gl_65_blk";
	};
	class aegis_weap_g36c_65_blk: aegis_g36c_base
	{
		scope = 2;
		author = "AveryTheKitty, Toadie2K";
		displayName = "G36C 6.5mm (Black)";
		baseWeapon = "aegis_weap_g36c_65_blk";
	};
	class Rifle_Long_Base_F: Rifle_Base_F
	{
		class GunParticles;
		class WeaponSlotsInfo;
	};
	class DMR_01_base_F: Rifle_Long_Base_F
	{
		class WeaponSlotsInfo;
	};
	class srifle_DMR_01_F: DMR_01_base_F
	{
		class WeaponSlotsInfo: WeaponSlotsInfo
		{
			class MuzzleSlot: asdg_MuzzleSlot_762R_SVD
			{
				iconPosition[] = {0,0.45};
				iconScale = 0.2;
			};
		};
	};
	class aegis_weap_vs121_blk: srifle_DMR_01_F
	{
		author = "AveryTheKitty";
		scope = 2;
		baseWeapon = "aegis_weap_vs121_blk";
		displayName = "VS-121 (Black)";
		picture = "\a3_aegis\weapons_f_aegis\longrangerifles\vs121\data\ui\icon_vs121_blk_ca.paa";
		hiddenSelectionsTextures[] = {"\a3_aegis\weapons_f_aegis\longrangerifles\vs121\data\vs121_01_blk_co.paa","\a3_aegis\weapons_f_aegis\longrangerifles\vs121\data\vs121_02_blk_co.paa"};
	};
	class DMR_06_base_F: Rifle_Long_Base_F
	{
		class WeaponSlotsInfo;
	};
	class srifle_DMR_06_camo_F: DMR_06_base_F
	{
		class WeaponSlotsInfo: WeaponSlotsInfo
		{
			class MuzzleSlot: asdg_MuzzleSlot_762
			{
				iconPosition[] = {0.06,0.4};
				iconScale = 0.15;
			};
			class CowsSlot: asdg_OpticRail1913_short
			{
				iconPosition[] = {0.52,0.36};
				iconScale = 0.15;
			};
			class UnderBarrelSlot: asdg_UnderSlot
			{
				iconPosition[] = {0.32,0.8};
				iconScale = 0.3;
			};
		};
	};
	class aegis_weap_m14_blk: srifle_DMR_06_camo_F
	{
		author = "AveryTheKitty";
		scope = 2;
		baseWeapon = "aegis_weap_m14_blk";
		displayName = "M14 Railed (Black)";
		picture = "\a3_aegis\weapons_f_aegis\longrangerifles\m14\data\ui\icon_m14_blk_ca.paa";
		hiddenSelectionsTextures[] = {"\a3_aegis\weapons_f_aegis\longrangerifles\m14\data\m14_01_blk_co.paa","\a3_aegis\weapons_f_aegis\longrangerifles\m14\data\m14_02_blk_co.paa"};
		magazines[] = {"20Rnd_762x51_Mag"};
	};
	class mk20_base_F: Rifle_Base_F
	{
		class WeaponSlotsInfo;
	};
	class arifle_Mk20_F: mk20_base_F
	{
		class WeaponSlotsInfo: WeaponSlotsInfo
		{
			class MuzzleSlot: asdg_MuzzleSlot_556
			{
				iconPosition[] = {0,0.36};
				iconScale = 0.2;
			};
		};
	};
	class arifle_Mk20_plain_F;
	class arifle_Mk20C_F: mk20_base_F
	{
		class WeaponSlotsInfo: WeaponSlotsInfo
		{
			class MuzzleSlot: asdg_MuzzleSlot_556
			{
				iconPosition[] = {0.1,0.36};
				iconScale = 0.2;
			};
		};
	};
	class arifle_Mk20C_plain_F;
	class arifle_Mk20_GL_F: mk20_base_F
	{
		class WeaponSlotsInfo: WeaponSlotsInfo
		{
			class MuzzleSlot: asdg_MuzzleSlot_556
			{
				iconPosition[] = {0.1,0.36};
				iconScale = 0.2;
			};
		};
	};
	class arifle_Mk20_GL_plain_F;
	class aegis_weap_f2000_blk: arifle_Mk20_plain_F
	{
		author = "AveryTheKitty";
		scope = 2;
		displayName = "F2000 (Black)";
		baseWeapon = "aegis_weap_f2000_blk";
		picture = "\a3_aegis\weapons_f_aegis\rifles\f2000\data\ui\icon_f2000_blk_ca.paa";
		hiddenSelectionsTextures[] = {"\a3_aegis\weapons_f_aegis\rifles\f2000\data\f2000_blk_co.paa"};
	};
	class aegis_weap_f2000c_blk: arifle_Mk20C_plain_F
	{
		author = "AveryTheKitty";
		scope = 2;
		displayName = "F2000 Carbine (Black)";
		baseWeapon = "aegis_weap_f2000_cqc_blk";
		picture = "\a3_aegis\weapons_f_aegis\rifles\f2000\data\ui\icon_f2000_cqc_blk_ca.paa";
		hiddenSelectionsTextures[] = {"\a3_aegis\weapons_f_aegis\rifles\f2000\data\f2000_blk_co.paa"};
	};
	class aegis_weap_f2000_gl_blk: arifle_Mk20_GL_plain_F
	{
		author = "AveryTheKitty";
		scope = 2;
		displayName = "F2000 GL (Black)";
		baseWeapon = "aegis_weap_f2000_gl_blk";
		picture = "\a3_aegis\weapons_f_aegis\rifles\f2000\data\ui\icon_f2000_gl_blk_ca.paa";
		hiddenSelectionsTextures[] = {"\a3_aegis\weapons_f_aegis\rifles\f2000\data\f2000_blk_co.paa","\a3_aegis\weapons_f_aegis\rifles\f2000\data\f2000_misc_blk_co.paa"};
	};
	class Tavor_base_F: Rifle_Base_F
	{
		class WeaponSlotsInfo;
		class Single: Mode_SemiAuto
		{
			reloadTime = 0.066;
		};
		class FullAuto: Mode_FullAuto
		{
			reloadTime = 0.066;
		};
	};
	class arifle_TRG20_F: Tavor_base_F
	{
		class WeaponSlotsInfo: WeaponSlotsInfo
		{
			class MuzzleSlot: asdg_MuzzleSlot_556
			{
				iconPosition[] = {0,0.4};
				iconScale = 0.2;
			};
		};
	};
	class arifle_TRG21_F: Tavor_base_F
	{
		hiddenSelections[] = {"camo"};
		class WeaponSlotsInfo: WeaponSlotsInfo
		{
			class MuzzleSlot: asdg_MuzzleSlot_556
			{
				iconPosition[] = {0,0.4};
				iconScale = 0.2;
			};
		};
	};
	class arifle_TRG21_GL_F: Tavor_base_F
	{
		class WeaponSlotsInfo: WeaponSlotsInfo
		{
			class MuzzleSlot: asdg_MuzzleSlot_556
			{
				iconPosition[] = {0,0.4};
				iconScale = 0.2;
			};
		};
	};
	class aegis_weap_tar21_blk: arifle_TRG21_F
	{
		author = "AveryTheKitty";
		displayName = "Tavor TAR-21 (Black)";
		baseWeapon = "aegis_weap_tar21_blk";
		picture = "\a3_aegis\weapons_f_aegis\rifles\tavor\data\ui\icon_tavor_blk_ca.paa";
		hiddenSelectionsTextures[] = {"\a3_aegis\weapons_f_aegis\rifles\tavor\data\tavor_blk_co.paa"};
		class Single;
		class FullAuto;
	};
	class aegis_weap_tar21_cqc_blk: arifle_TRG20_F
	{
		author = "AveryTheKitty";
		displayName = "Tavor CTAR-21 (Black)";
		baseWeapon = "aegis_weap_tar21_cqc_blk";
		picture = "\a3_aegis\weapons_f_aegis\rifles\tavor\data\ui\icon_tavor_cqc_blk_ca.paa";
		hiddenSelectionsTextures[] = {"\a3_aegis\weapons_f_aegis\rifles\tavor\data\tavor_blk_co.paa"};
		class Single;
		class FullAuto;
	};
	class aegis_weap_tar21_gl_blk: arifle_TRG21_GL_F
	{
		author = "AveryTheKitty";
		displayName = "Tavor TAR-21 GL (Black)";
		baseWeapon = "aegis_weap_tar21_gl_blk";
		picture = "\a3_aegis\weapons_f_aegis\rifles\tavor\data\ui\icon_tavor_gl_blk_ca.paa";
		hiddenSelectionsTextures[] = {"\a3_aegis\weapons_f_aegis\rifles\tavor\data\tavor_blk_co.paa","\a3\weapons_f\rifles\trg20\data\tar21_eglm_co.paa","\a3\weapons_f\data\gl_holo_co.paa"};
		class Single;
		class FullAuto;
	};
	class aegis_weap_fort652_blk: aegis_weap_tar21_blk
	{
		displayName = "Fort-652 6.5mm (Black)";
		baseWeapon = "aegis_weap_fort652_blk";
		recoil = "recoil_aegis_sa80";
		magazines[] = {"30Rnd_65x39_caseless_msbs_mag","30Rnd_65x39_caseless_msbs_mag_Tracer"};
		magazineWell[] = {"MX_65x39_MSBS"};
		class Single: Single
		{
			class StandardSound
			{
				soundSetShot[] = {"jsrs_type115_shot_soundset","jsrs_6x5mm_reverb_soundset"};
			};
			class SilencedSound
			{
				soundSetShot[] = {"jsrs_mx_shot_silenced_soundset","jsrs_6x5mm_sd_reverb_soundset"};
			};
		};
		class FullAuto: FullAuto
		{
			class StandardSound
			{
				soundSetShot[] = {"jsrs_type115_shot_soundset","jsrs_6x5mm_reverb_soundset"};
			};
			class SilencedSound
			{
				soundSetShot[] = {"jsrs_mx_shot_silenced_soundset","jsrs_6x5mm_sd_reverb_soundset"};
			};
		};
	};
	class aegis_weap_fort652_gl_blk: aegis_weap_tar21_gl_blk
	{
		displayName = "Fort-652 GL 6.5mm (Black)";
		baseWeapon = "aegis_weap_fort652_gl_blk";
		recoil = "recoil_aegis_sa80";
		magazines[] = {"30Rnd_65x39_caseless_msbs_mag","30Rnd_65x39_caseless_msbs_mag_Tracer"};
		magazineWell[] = {"MX_65x39_MSBS"};
		class Single: Single
		{
			class StandardSound
			{
				soundSetShot[] = {"jsrs_type115_shot_soundset","jsrs_6x5mm_reverb_soundset"};
			};
			class SilencedSound
			{
				soundSetShot[] = {"jsrs_mx_shot_silenced_soundset","jsrs_6x5mm_sd_reverb_soundset"};
			};
		};
		class FullAuto: FullAuto
		{
			class StandardSound
			{
				soundSetShot[] = {"jsrs_type115_shot_soundset","jsrs_6x5mm_reverb_soundset"};
			};
			class SilencedSound
			{
				soundSetShot[] = {"jsrs_mx_shot_silenced_soundset","jsrs_6x5mm_sd_reverb_soundset"};
			};
		};
	};
	class aegis_weap_fort651_blk: aegis_weap_tar21_cqc_blk
	{
		displayName = "Fort-651 6.5mm (Black)";
		baseWeapon = "aegis_weap_fort651_blk";
		recoil = "recoil_aegis_sa80";
		magazines[] = {"30Rnd_65x39_caseless_msbs_mag","30Rnd_65x39_caseless_msbs_mag_Tracer"};
		magazineWell[] = {"MX_65x39_MSBS"};
		class Single: Single
		{
			class StandardSound
			{
				soundSetShot[] = {"jsrs_type115_shot_soundset","jsrs_6x5mm_reverb_soundset"};
			};
			class SilencedSound
			{
				soundSetShot[] = {"jsrs_mx_shot_silenced_soundset","jsrs_6x5mm_sd_reverb_soundset"};
			};
		};
		class FullAuto: FullAuto
		{
			class StandardSound
			{
				soundSetShot[] = {"jsrs_type115_shot_soundset","jsrs_6x5mm_reverb_soundset"};
			};
			class SilencedSound
			{
				soundSetShot[] = {"jsrs_mx_shot_silenced_soundset","jsrs_6x5mm_sd_reverb_soundset"};
			};
		};
	};
	class arifle_AK12_F;
	class arifle_AK12U_F;
	class arifle_AK12_GL_F;
	class arifle_RPK12_F;
	class aegis_weap_ncar15_blk: arifle_AK12_F
	{
		scope = 2;
		author = "Ravenholme";
		displayName = "NCAR-15 5.8mm (Black)";
		baseWeapon = "aegis_weap_ncar15";
		magazines[] = {"30Rnd_580x42_Mag_F","30Rnd_580x42_Mag_Tracer_F"};
		magazineWell[] = {"CTAR_580x42","CTAR_580x42_Large"};
	};
	class aegis_weap_ncar15_gl_blk: arifle_AK12_GL_F
	{
		scope = 2;
		author = "Ravenholme";
		displayName = "NCAR-15 GL 5.8mm (Black)";
		baseWeapon = "aegis_weap_ncar15_gl_blk";
		magazines[] = {"30Rnd_580x42_Mag_F","30Rnd_580x42_Mag_Tracer_F"};
		magazineWell[] = {"CTAR_580x42","CTAR_580x42_Large"};
	};
	class aegis_weap_ncar15_carbine_blk: arifle_AK12U_F
	{
		scope = 2;
		author = "Ravenholme";
		displayName = "NCAR-15 Carbine 5.8mm (Black)";
		baseWeapon = "aegis_weap_ncar15_carbine_blk";
		magazines[] = {"30Rnd_580x42_Mag_F","30Rnd_580x42_Mag_Tracer_F"};
		magazineWell[] = {"CTAR_580x42","CTAR_580x42_Large"};
	};
	class aegis_weap_ncar15_lsw_blk: arifle_RPK12_F
	{
		scope = 2;
		author = "Ravenholme";
		displayName = "NCAR-15 LSW 5.8mm (Black)";
		baseWeapon = "aegis_weap_ncar15_lsw_blk";
		magazines[] = {"100Rnd_580x42_Mag_F","100Rnd_580x42_Mag_Tracer_F"};
		magazineWell[] = {"CTAR_580x42","CTAR_580x42_Large"};
	};
	class launch_MRAWS_base_F;
	class launch_MRAWS_olive_rail_F;
	class aegis_weap_mraws_blk: launch_MRAWS_base_F
	{
		author = "POLPOX";
		scope = 2;
		baseWeapon = "aegis_mraws_blk";
		displayName = "MAAWS Mk4 Mod 1 Launcher (Black)";
		picture = "\a3_aegis\weapons_f_aegis\launchers\mraws\data\ui\icon_mraws_black_ca.paa";
		hiddenSelectionsTextures[] = {"\a3_aegis\weapons_f_aegis\launchers\mraws\data\mraws_black_co.paa","\a3\weapons_f_tank\launchers\mraws\data\launch_mraws_02_f_co.paa"};
	};
	class aegis_weap_mraws_rail_blk: launch_MRAWS_olive_rail_F
	{
		author = "POLPOX";
		scope = 2;
		baseWeapon = "aegis_mraws_rail_blk";
		displayName = "MAAWS Mk4 Mod 0 Launcher (Black)";
		picture = "\a3_aegis\weapons_f_aegis\launchers\mraws\data\ui\icon_mraws_black_rail_ca.paa";
		hiddenSelectionsTextures[] = {"\a3_aegis\weapons_f_aegis\launchers\mraws\data\mraws_black_co.paa","\a3\weapons_f_tank\launchers\mraws\data\launch_mraws_rail_02_f_co.paa"};
	};
	class arifle_MX_Base_F: Rifle_Base_F
	{
		class WeaponSlotsInfo;
	};
	class arifle_MXC_F: arifle_MX_Base_F
	{
		class WeaponSlotsInfo: WeaponSlotsInfo
		{
			class MuzzleSlot: asdg_MuzzleSlot_556
			{
				iconPosition[] = {0,0.4};
				iconScale = 0.2;
			};
			class PointerSlot: asdg_FrontSideRail
			{
				iconPosition[] = {0.2,0.4};
				iconScale = 0.25;
			};
		};
	};
	class arifle_MX_F: arifle_MX_Base_F
	{
		class WeaponSlotsInfo: WeaponSlotsInfo
		{
			class MuzzleSlot: asdg_MuzzleSlot_556
			{
				iconPosition[] = {0,0.45};
				iconScale = 0.2;
			};
			class PointerSlot: asdg_FrontSideRail
			{
				iconPosition[] = {0.2,0.45};
				iconScale = 0.25;
			};
		};
	};
	class arifle_MX_GL_F: arifle_MX_Base_F
	{
		class WeaponSlotsInfo: WeaponSlotsInfo
		{
			class MuzzleSlot: asdg_MuzzleSlot_556
			{
				iconPosition[] = {0,0.45};
				iconScale = 0.2;
			};
			class PointerSlot: asdg_FrontSideRail
			{
				iconPosition[] = {0.2,0.45};
				iconScale = 0.25;
			};
		};
	};
	class arifle_MX_SW_F: arifle_MX_Base_F
	{
		class WeaponSlotsInfo: WeaponSlotsInfo
		{
			class MuzzleSlot: asdg_MuzzleSlot_556
			{
				iconPosition[] = {0,0.45};
				iconScale = 0.2;
			};
			class PointerSlot: asdg_FrontSideRail
			{
				iconPosition[] = {0.2,0.45};
				iconScale = 0.25;
			};
		};
	};
	class arifle_MXM_F: arifle_MX_Base_F
	{
		class WeaponSlotsInfo: WeaponSlotsInfo
		{
			class MuzzleSlot: asdg_MuzzleSlot_556
			{
				iconPosition[] = {0,0.4};
				iconScale = 0.2;
			};
			class PointerSlot: asdg_FrontSideRail
			{
				iconPosition[] = {0.2,0.45};
				iconScale = 0.25;
			};
		};
	};
	class LMG_Zafir_F: Rifle_Long_Base_F
	{
		class WeaponSlotsInfo: WeaponSlotsInfo
		{
			class MuzzleSlot: asdg_MuzzleSlot_762R_PK
			{
				iconPosition[] = {0.05,0.38};
				iconScale = 0.2;
			};
		};
	};
	class aegis_weap_zafir_blk: LMG_Zafir_F
	{
		author = "AveryTheKitty";
		displayName = "Negev NG7 (Black)";
		picture = "\a3_aegis\weapons_f_aegis\machineguns\zafir\data\ui\icon_lmg_zafir_black_f_x_ca.paa";
		baseWeapon = "aegis_weap_zafir_blk";
		hiddenSelectionsTextures[] = {"\a3_aegis\weapons_f_aegis\machineguns\zafir\data\zafir01_black_co.paa","\a3_aegis\weapons_f_aegis\machineguns\zafir\data\zafir02_black_co.paa"};
	};
	class aegis_weap_zafir_ghex: LMG_Zafir_F
	{
		author = "AveryTheKitty";
		displayName = "Negev NG7 (Green Hex)";
		picture = "\a3_aegis\weapons_f_aegis\machineguns\zafir\data\ui\icon_lmg_zafir_ghex_f_x_ca.paa";
		baseWeapon = "aegis_weap_zafir_ghex";
		hiddenSelectionsTextures[] = {"\a3_aegis\weapons_f_aegis\machineguns\zafir\data\lmg_zafir_ghex_f_1_co.paa","\a3_aegis\weapons_f_aegis\machineguns\zafir\data\lmg_zafir_ghex_f_2_co.paa"};
	};
	class MMG_01_base_F;
	class MMG_01_hex_F: MMG_01_base_F
	{
		recoil = "recoil_aegis_hk121";
	};
	class aegis_weap_hk121_blk: MMG_01_hex_F
	{
		author = "AveryTheKitty";
		displayName = "HK121 (Black)";
		picture = "\a3_aegis\weapons_f_aegis\machineguns\mmg_01\data\ui\icon_mmg_01_black_f_x_ca.paa";
		uiPicture = "\a3\weapons_f\data\ui\icon_mg_ca.paa";
		baseWeapon = "aegis_weap_hk121_blk";
		hiddenSelectionsTextures[] = {"\a3_aegis\weapons_f_aegis\machineguns\mmg_01\data\mmg_01_01_black_co.paa","\a3_aegis\weapons_f_aegis\machineguns\mmg_01\data\mmg_01_02_black_co.paa","\a3_aegis\weapons_f_aegis\machineguns\mmg_01\data\mmg_01_03_black_co.paa"};
		hiddenSelectionsMaterials[] = {"\a3_aegis\weapons_f_aegis\machineguns\mmg_01\data\mmg_01_01_black.rvmat","\a3_aegis\weapons_f_aegis\machineguns\mmg_01\data\mmg_01_02_black.rvmat","\a3_aegis\weapons_f_aegis\machineguns\mmg_01\data\mmg_01_03_black.rvmat"};
		class LinkedItems{};
	};
	class aegis_weap_hk121_ghex: MMG_01_hex_F
	{
		author = "AveryTheKitty";
		displayName = "HK121 (Green Hex)";
		picture = "\a3_aegis\weapons_f_aegis\machineguns\mmg_01\data\ui\icon_mmg_01_ghex_f_x_ca.paa";
		uiPicture = "\a3\weapons_f\data\ui\icon_mg_ca.paa";
		baseWeapon = "aegis_weap_hk121_ghex";
		hiddenSelectionsTextures[] = {"\a3_aegis\weapons_f_aegis\machineguns\mmg_01\data\mmg_01_01_ghex_co.paa","\a3_aegis\weapons_f_aegis\machineguns\mmg_01\data\mmg_01_02_ghex_co.paa","\a3_aegis\weapons_f_aegis\machineguns\mmg_01\data\mmg_01_03_ghex_co.paa"};
		hiddenSelectionsMaterials[] = {"\a3_aegis\weapons_f_aegis\machineguns\mmg_01\data\mmg_01_01_ghex.rvmat","\a3_aegis\weapons_f_aegis\machineguns\mmg_01\data\mmg_01_02_ghex.rvmat","\a3_aegis\weapons_f_aegis\machineguns\mmg_01\data\mmg_01_03_ghex.rvmat"};
		class LinkedItems{};
	};
	class MMG_02_base_F;
	class MMG_02_camo_F: MMG_02_base_F
	{
		recoil = "recoil_aegis_lwmmg";
	};
	class SMG_01_F;
	class aegis_weap_vector_blk: SMG_01_F
	{
		author = "AveryTheKitty";
		displayName = "Vector SMG (Black)";
		picture = "\a3_aegis\weapons_f_aegis\smgs\smg_01\data\ui\icon_smg_01_black_f_x_ca.paa";
		baseWeapon = "aegis_weap_vector_blk";
		hiddenSelectionsTextures[] = {"\a3_aegis\weapons_f_aegis\smgs\smg_01\data\smg_01_black_co.paa","\a3_aegis\weapons_f_aegis\smgs\smg_01\data\vectoratt_black_co.paa","\a3\weapons_f\acc\data\battlesight_co.paa"};
		hiddenSelectionsMaterials[] = {"\a3_aegis\weapons_f_aegis\smgs\smg_01\data\smg_01_black.rvmat","\a3_aegis\weapons_f_aegis\smgs\smg_01\data\vectoratt_black.rvmat","\a3\weapons_f\acc\data\battlesight.rvmat"};
	};
	class hgun_ACPC2_F;
	class hgun_Pistol_heavy_01_green_F;
	class aegis_weap_cc2_blk: hgun_ACPC2_F
	{
		author = "AveryTheKitty";
		displayName = "Custom Covert II (Black)";
		picture = "\a3_aegis\weapons_f_aegis\pistols\acpc2\data\ui\icon_hgun_acpc2_black_f_x_ca.paa";
		baseWeapon = "aegis_weap_cc2_blk";
		hiddenSelectionsTextures[] = {"\a3_aegis\weapons_f_aegis\pistols\acpc2\data\acpc2_black_co.paa"};
		hiddenSelectionsMaterials[] = {"\a3_aegis\weapons_f_aegis\pistols\acpc2\data\acpc2_black.rvmat"};
	};
	class aegis_weap_fnx45_blk: hgun_Pistol_heavy_01_green_F
	{
		author = "$AveryTheKitty";
		displayName = "FNX-45 Tactical (Black)";
		picture = "\a3_aegis\weapons_f_aegis\pistols\pistol_heavy_01\data\ui\icon_hgun_pistol_heavy_01_black_f_x_ca.paa";
		baseWeapon = "aegis_weap_fnx45_blk";
		hiddenSelectionsTextures[] = {"\a3_aegis\weapons_f_aegis\pistols\pistol_heavy_01\data\pistol_heavy_01_black_co.paa"};
	};
	class launch_RPG32_F;
	class launch_RPG32_camo_F;
	class aegis_weap_rpg32_blk: launch_RPG32_F
	{
		scope = 2;
		author = "AveryTheKitty";
		baseWeapon = "aegis_weap_rpg32_blk";
		displayName = "RPG-32 (Black)";
		picture = "\a3_aegis\weapons_f_aegis\launchers\rpg32\data\ui\icon_rpg32_black_ca.paa";
		hiddenSelectionsTextures[] = {"\a3_aegis\weapons_f_aegis\launchers\rpg32\data\rpg32_black_co.paa","\a3\weapons_f\launchers\rpg32\data\rpg_32_optics_co.paa"};
	};
	class aegis_weap_rpg32_camo: launch_RPG32_camo_F
	{
		scope = 2;
		author = "AveryTheKitty";
		displayName = "RPG-32 (Camo)";
	};
	class ItemCore;
	class optic_MRCO: ItemCore
	{
		class ItemInfo;
	};
	class aegis_acc_lrco_blk: optic_MRCO
	{
		scope = 2;
		author = "AveryTheKitty";
		displayName = "LRCO (Black)";
		descriptionShort = "LRCO";
		picture = "\a3_aegis\weapons_f_aegis\acc\data\ui\icon_lrco_blk_ca.paa";
		model = "\a3_aegis\weapons_f_aegis\acc\lrco_blk";
		class ItemInfo: ItemInfo
		{
			modelOptics = "\a3_aegis\weapons_f_aegis\acc\lrco_blk";
		};
	};
	class aegis_acc_lrco_sand: aegis_acc_lrco_blk
	{
		displayName = "LRCO (Sand)";
		picture = "\a3_aegis\weapons_f_aegis\acc\data\ui\icon_lrco_snd_ca.paa";
		model = "\a3_aegis\weapons_f_aegis\acc\lrco_snd";
		class ItemInfo: ItemInfo
		{
			modelOptics = "\a3_aegis\weapons_f_aegis\acc\lrco_snd";
		};
	};
	class Binocular;
	class NVGoggles: Binocular
	{
		class ItemInfo;
	};
	class nvg_goggles_cbr: NVGoggles
	{
		scope = 2;
		author = "AveryTheKitty";
		displayName = "Goggles Raised (Coyote)";
		descriptionShort = "$str_a3_a_cfgweapons_goggles1";
		modelOptics = "\a3\weapons_f\reticle\optics_empty";
		model = "\a3_aegis\weapons_f_aegis\binocular\goggles";
		picture = "\a3\characters_f\data\ui\icon_g_combat_ca.paa";
		visionMode[] = {"Normal"};
		class ItemInfo: ItemInfo
		{
			uniformModel = "\a3_aegis\weapons_f_aegis\binocular\goggles";
			modelOff = "\a3_aegis\weapons_f_aegis\binocular\goggles";
			mass = 6;
		};
	};
	class nvg_goggles_grn: nvg_goggles_cbr
	{
		displayName = "Goggles Raised (Green)";
		model = "\a3_aegis\weapons_f_aegis\binocular\goggles_grn_f";
		picture = "\a3\characters_f_exp\blufor\data\ui\icon_g_combat_goggles_tna_f_ca.paa";
		class ItemInfo: ItemInfo
		{
			uniformModel = "\a3_aegis\weapons_f_aegis\binocular\goggles_grn_f";
			modelOff = "\a3_aegis\weapons_f_aegis\binocular\goggles_grn_f";
		};
	};
	class nvg_goggles_tropic: nvg_goggles_cbr
	{
		displayName = "Goggles Raised (Tropic)";
		model = "\a3_aegis\weapons_f_aegis\binocular\goggles_tna_f";
		picture = "\a3\characters_f_exp\blufor\data\ui\icon_g_combat_goggles_tna_f_ca.paa";
		class ItemInfo: ItemInfo
		{
			uniformModel = "\a3_aegis\weapons_f_aegis\binocular\goggles_tna_f";
			modelOff = "\a3_aegis\weapons_f_aegis\binocular\goggles_tna_f";
		};
	};
	class nvg_scrim_wdl: NVGoggles
	{
		scope = 2;
		author = "Ianassa";
		displayName = "Helmet Scrim (Woodland)";
		descriptionShort = "Helmet Scrim";
		model = "\a3\characters_f\blufor\headgear_b_helmet_camo";
		modelOptics = "\a3\weapons_f\reticle\optics_empty";
		picture = "\a3_aegis\weapons_f_aegis\binocular\data\ui\icon_scrim_ca.paa";
		hiddenSelections[] = {"camo1","camo2"};
		hiddenSelectionsTextures[] = {"","\a3_aegis\weapons_f_aegis\binocular\data\scrim_wood_ca.paa"};
		visionMode[] = {"Normal"};
		class ItemInfo: ItemInfo
		{
			uniformModel = "\a3\characters_f\blufor\headgear_b_helmet_camo";
			modelOff = "\a3\characters_f\blufor\headgear_b_helmet_camo";
			mass = 6;
			hiddenSelections[] = {"camo1","camo2"};
			hiddenSelectionsTextures[] = {"","\a3_aegis\weapons_f_aegis\binocular\data\scrim_wood_ca.paa"};
		};
	};
	class nvg_scrim_wdl_grass: nvg_scrim_wdl
	{
		displayName = "Helmet Scrim (Woodland, Grass)";
		hiddenSelectionsTextures[] = {"","\a3_aegis\weapons_f_aegis\binocular\data\scrim_wood_grass_ca.paa"};
		class ItemInfo: ItemInfo
		{
			hiddenSelectionsTextures[] = {"","\a3_aegis\weapons_f_aegis\binocular\data\scrim_wood_grass_ca.paa"};
		};
	};
	class nvg_scrim_wdl_leaves_1: nvg_scrim_wdl
	{
		displayName = "Helmet Scrim (Woodland, Leaves 1)";
		hiddenSelectionsTextures[] = {"","\a3_aegis\weapons_f_aegis\binocular\data\scrim_wood_leaves_1_ca.paa"};
		class ItemInfo: ItemInfo
		{
			hiddenSelectionsTextures[] = {"","\a3_aegis\weapons_f_aegis\binocular\data\scrim_wood_leaves_1_ca.paa"};
		};
	};
	class nvg_scrim_wdl_leaves_2: nvg_scrim_wdl
	{
		displayName = "Helmet Scrim (Woodland, Leaves 2)";
		hiddenSelectionsTextures[] = {"","\a3_aegis\weapons_f_aegis\binocular\data\scrim_wood_leaves_2_ca.paa"};
		class ItemInfo: ItemInfo
		{
			hiddenSelectionsTextures[] = {"","\a3_aegis\weapons_f_aegis\binocular\data\scrim_wood_leaves_2_ca.paa"};
		};
	};
	class nvg_scrim_wdl_leaves_3: nvg_scrim_wdl
	{
		displayName = "Helmet Scrim (Woodland, Leaves 3)";
		hiddenSelectionsTextures[] = {"","\a3_aegis\weapons_f_aegis\binocular\data\scrim_wood_leaves_3_ca.paa"};
		class ItemInfo: ItemInfo
		{
			hiddenSelectionsTextures[] = {"","\a3_aegis\weapons_f_aegis\binocular\data\scrim_wood_leaves_3_ca.paa"};
		};
	};
	class nvg_scrim_wdl_pine: nvg_scrim_wdl
	{
		displayName = "Helmet Scrim (Woodland, Pine)";
		hiddenSelectionsTextures[] = {"","\a3_aegis\weapons_f_aegis\binocular\data\scrim_wood_pine_ca.paa"};
		class ItemInfo: ItemInfo
		{
			hiddenSelectionsTextures[] = {"","\a3_aegis\weapons_f_aegis\binocular\data\scrim_wood_pine_ca.paa"};
		};
	};
	class nvg_scrim_snow: nvg_scrim_wdl
	{
		displayName = "Helmet Scrim (Snow)";
		picture = "\a3_aegis\weapons_f_aegis\binocular\data\ui\icon_scrim_snow_ca.paa";
		hiddenSelectionsTextures[] = {"","\a3_aegis\weapons_f_aegis\binocular\data\scrim_snow_ca.paa"};
		class ItemInfo: ItemInfo
		{
			hiddenSelectionsTextures[] = {"","\a3_aegis\weapons_f_aegis\binocular\data\scrim_snow_ca.paa"};
		};
	};
	class nvg_scrim_snow_pine: nvg_scrim_snow
	{
		displayName = "Helmet Scrim (Snow, Pine)";
		hiddenSelectionsTextures[] = {"","\a3_aegis\weapons_f_aegis\binocular\data\scrim_snow_pine_ca.paa"};
		class ItemInfo: ItemInfo
		{
			hiddenSelectionsTextures[] = {"","\a3_aegis\weapons_f_aegis\binocular\data\scrim_snow_pine_ca.paa"};
		};
	};
};
