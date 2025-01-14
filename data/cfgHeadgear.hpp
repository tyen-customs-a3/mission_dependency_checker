class HeadgearItem: InventoryItem_Base_F
{
	allowedSlots[] = {BACKPACK_SLOT, HEADGEAR_SLOT};
	type = HEADGEAR_SLOT;
	hiddenSelections[] = {};
	hitpointName = "HitHead";
};
class H_Booniehat_mcamo;
class CUP_H_USArmy_Boonie_UCP: H_Booniehat_mcamo
{
	CUP_HEADER;
	displayname = "Booniehat (UCP)";
	descriptionShort = "$STR_A3_SP_NOARMOR";
	hiddenSelectionsTextures[] = { "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\data\cup_boonie_acu_co.paa" };
	model = "\A3\Characters_F\Common\booniehat";
	picture = "\A3\characters_f\Data\UI\icon_H_booniehat_desert_ca.paa";
	class ItemInfo: HeadgearItem {
		allowedslots[] = {801, 901, 701, 605};
		armor = "3*0";			mass = 10;
		modelsdes[] = {6};
		passthrough = 0.8;
		hiddenSelections[] = {"Camo"};
		uniformmodel = "\A3\Characters_F\Common\booniehat";
		#include "\CUP\Creatures\hitpoints_headno.h"
	};
};
class CUP_M_USArmy_Boonie : CUP_H_USArmy_Boonie_UCP
{
	CUP_HEADER_PROTECTED;
};

class CUP_H_USArmy_Boonie_hs_UCP: H_Booniehat_mcamo
{
	CUP_HEADER;
	displayname = "Booniehat (Headset/UCP)";
	descriptionShort = "$STR_A3_SP_NOARMOR";
	hiddenSelectionsTextures[] = { "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\data\cup_boonie_acu_co.paa" };
	model = "A3\Characters_F_EPB\Common\booniehat_hs.p3d";
	picture = "\A3\characters_f\Data\UI\icon_H_booniehat_desert_ca.paa";
	class ItemInfo: HeadgearItem {
		allowedslots[] = {801, 901, 701, 605};
		armor = "3*0";			mass = 10;
		modelsdes[] = {6};
		passthrough = 0.8;
		hiddenSelections[] = {"Camo"};
		uniformmodel = "A3\Characters_F_EPB\Common\booniehat_hs.p3d";
		#include "\CUP\Creatures\hitpoints_headno.h"
	};
};

class CUP_H_USArmy_Boonie_OCP: H_Booniehat_mcamo
{
	CUP_HEADER;
	displayname = "Booniehat (OCP)";
	descriptionShort = "$STR_A3_SP_NOARMOR";
	hiddenSelectionsTextures[] = { "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\data\cup_boonie_ocp_co.paa" };
	model = "\A3\Characters_F\Common\booniehat";
	picture = "\A3\characters_f\Data\UI\icon_H_booniehat_desert_ca.paa";
	class ItemInfo: HeadgearItem {
		allowedslots[] = {801, 901, 701, 605};
		armor = "3*0";			mass = 10;
		modelsdes[] = {6};
		passthrough = 0.8;
		hiddenSelections[] = {"Camo"};
		uniformmodel = "\A3\Characters_F\Common\booniehat";
		#include "\CUP\Creatures\hitpoints_headno.h"
	};
};

class CUP_H_USArmy_Boonie_hs_OCP: H_Booniehat_mcamo
{
	CUP_HEADER;
	displayname = "Booniehat (Headset/OCP)";
	descriptionShort = "$STR_A3_SP_NOARMOR";
	hiddenSelectionsTextures[] = { "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\data\cup_boonie_ocp_co.paa" };
	model = "A3\Characters_F_EPB\Common\booniehat_hs.p3d";
	picture = "\A3\characters_f\Data\UI\icon_H_booniehat_desert_ca.paa";
	class ItemInfo: HeadgearItem {
		allowedslots[] = {801, 901, 701, 605};
		armor = "3*0";			mass = 10;
		modelsdes[] = {6};
		passthrough = 0.8;
		hiddenSelections[] = {"Camo"};
		uniformmodel = "A3\Characters_F_EPB\Common\booniehat_hs.p3d";
		#include "\CUP\Creatures\hitpoints_headno.h"
	};
};

class CUP_H_USArmy_Boonie_OEFCP: H_Booniehat_mcamo
{
	CUP_HEADER;
	displayname = "Booniehat (OEF-CP)";
	descriptionShort = "$STR_A3_SP_NOARMOR";
	hiddenSelectionsTextures[] = { "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\data\cup_boonie_oefcp_co.paa" };
	model = "\A3\Characters_F\Common\booniehat";
	picture = "\A3\characters_f\Data\UI\icon_H_booniehat_desert_ca.paa";
	class ItemInfo: HeadgearItem {
		allowedslots[] = {801, 901, 701, 605};
		armor = "3*0";			mass = 10;
		modelsdes[] = {6};
		passthrough = 0.8;
		hiddenSelections[] = {"Camo"};
		uniformmodel = "\A3\Characters_F\Common\booniehat";
		#include "\CUP\Creatures\hitpoints_headno.h"
	};
};

class CUP_H_USArmy_Boonie_hs_OEFCP: H_Booniehat_mcamo
{
	CUP_HEADER;
	displayname = "Booniehat (Headset/OEF-CP)";
	descriptionShort = "$STR_A3_SP_NOARMOR";
	hiddenSelectionsTextures[] = { "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\data\cup_boonie_oefcp_co.paa" };
	model = "A3\Characters_F_EPB\Common\booniehat_hs.p3d";
	picture = "\A3\characters_f\Data\UI\icon_H_booniehat_desert_ca.paa";
	class ItemInfo: HeadgearItem {
		allowedslots[] = {801, 901, 701, 605};
		armor = "3*0";			mass = 10;
		modelsdes[] = {6};
		passthrough = 0.8;
		hiddenSelections[] = {"Camo"};
		uniformmodel = "A3\Characters_F_EPB\Common\booniehat_hs.p3d";
		#include "\CUP\Creatures\hitpoints_headno.h"
	};
};

class CUP_H_USA_Boonie_wdl: ItemCore
{
	CUP_HEADER_PUBLIC;
	displayName  = "Boonie (M81)";
	descriptionShort = "$STR_A3_SP_NOARMOR";
	picture = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_ACR\data\ui\icon_acr_hat02.paa";
	model   = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_ACR\CUP_ACR_Hat02.p3d";
	hiddenSelections[] = {"camo2", "camo3"};
	hiddenSelectionsTextures[] = {
			"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_ACR\data\equip1_co.paa",
			"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\data\booniefolded_M81_co.paa"
	};
	class ItemInfo: HeadgearItem
	{
		mass = 10;
		uniformModel = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_ACR\CUP_ACR_Hat02.p3d";
		allowedSlots[] = {UNIFORM_SLOT, BACKPACK_SLOT, VEST_SLOT, HEADGEAR_SLOT};
		modelSides[] = {6};
		armor = 0;
		passThrough = 1;
		hiddenSelections[] = {"camo2", "camo3"};
		hiddenSelectionsTextures[] = {
				"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_ACR\data\equip1_co.paa",
				"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\data\booniefolded_M81_co.paa"
		};
		#include "\CUP\Creatures\hitpoints_headno.h"
	};
};
class CUP_H_USA_Cap: ItemCore
{
	CUP_HEADER_PROTECTED;
	displayName  = "Cap (ACU)";
	descriptionShort = "$STR_A3_SP_NOARMOR";
	picture = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_PMC\data\ui\icon_h_pmc_cap_grey_ca.paa";
	model   = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USarmy\CUP_h_usarmy_cap.p3d";
	hiddenSelections[] = {"Camo1"};
	hiddenSelectionsTextures[] = {"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USarmy\data\tex4_co.paa"};
	class ItemInfo: HeadgearItem
	{
		mass = 10;
		uniformModel = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USarmy\CUP_h_usarmy_cap.p3d";
		allowedSlots[] = {UNIFORM_SLOT, BACKPACK_SLOT, VEST_SLOT, HEADGEAR_SLOT};
		modelSides[] = {6};
		armor = 0;
		passThrough = 1;
		hiddenSelections[] = {"Camo1"};
		#include "\CUP\Creatures\hitpoints_headno.h"
	};
};

class CUP_H_USA_Cap_Mcam_DEF: ItemCore
{
	CUP_HEADER_PUBLIC;
	displayName  = "Cap w/DEF (US Multicam)";
	descriptionShort = "$STR_A3_SP_NOARMOR";
	picture = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_PMC\data\ui\icon_h_pmc_cap_prr_tan_ca.paa";
	model   = "\A3\Characters_F\common\capb_headphones.p3d";
	hiddenSelections[] = {"camo"};
	hiddenSelectionsTextures[] = {"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\data\cap_def_mcam_co.paa"};
	class ItemInfo: HeadgearItem
	{
		mass = 10;
		uniformModel = "\A3\Characters_F\common\capb_headphones.p3d";
		allowedSlots[] = {UNIFORM_SLOT, BACKPACK_SLOT, VEST_SLOT, HEADGEAR_SLOT};
		modelSides[] = {6};
		armor = 0;
		passThrough = 1;
		hiddenSelections[] = {"camo"};
		hiddenSelectionsTextures[] = {"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\data\cap_def_mcam_co.paa"};
		#include "\CUP\Creatures\hitpoints_headno.h"
	};
	ace_hearing_protection = 0.75;
	ace_hearing_lowerVolume = 0.5;
};

class CUP_H_USA_Cap_AU_DEF: ItemCore
{
	CUP_HEADER_PUBLIC;
	displayName  = "Cap w/DEF (Auburn)";
	descriptionShort = "$STR_A3_SP_NOARMOR";
	picture = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_PMC\data\ui\icon_h_pmc_cap_prr_tan_ca.paa";
	model   = "\A3\Characters_F\common\capb_headphones.p3d";
	hiddenSelections[] = {"camo"};
	hiddenSelectionsTextures[] = {"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\data\cap_def_aub_co.paa"};
	class ItemInfo: HeadgearItem
	{
		mass = 10;
		uniformModel = "\A3\Characters_F\common\capb_headphones.p3d";
		allowedSlots[] = {UNIFORM_SLOT, BACKPACK_SLOT, VEST_SLOT, HEADGEAR_SLOT};
		modelSides[] = {6};
		armor = 0;
		passThrough = 1;
		hiddenSelections[] = {"camo"};
		hiddenSelectionsTextures[] = {"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\data\cap_def_aub_co.paa"};
		#include "\CUP\Creatures\hitpoints_headno.h"
	};
	ace_hearing_protection = 0.75;
	ace_hearing_lowerVolume = 0.5;
};

class CUP_H_USA_Cap_UT_DEF: ItemCore
{
	CUP_HEADER_PUBLIC;
	displayName  = "Cap w/DEF (Texas)";
	descriptionShort = "$STR_A3_SP_NOARMOR";
	picture = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_PMC\data\ui\icon_h_pmc_cap_prr_tan_ca.paa";
	model   = "\A3\Characters_F\common\capb_headphones.p3d";
	hiddenSelections[] = {"camo"};
	hiddenSelectionsTextures[] = {"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\data\cap_def_tex_co.paa"};
	class ItemInfo: HeadgearItem
	{
		mass = 10;
		uniformModel = "\A3\Characters_F\common\capb_headphones.p3d";
		allowedSlots[] = {UNIFORM_SLOT, BACKPACK_SLOT, VEST_SLOT, HEADGEAR_SLOT};
		modelSides[] = {6};
		armor = 0;
		passThrough = 1;
		hiddenSelections[] = {"camo"};
		hiddenSelectionsTextures[] = {"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\data\cap_def_tex_co.paa"};
		#include "\CUP\Creatures\hitpoints_headno.h"
	};
	ace_hearing_protection = 0.75;
	ace_hearing_lowerVolume = 0.5;
};

class CUP_H_USA_Cap_NY_DEF: ItemCore
{
	CUP_HEADER_PUBLIC;
	displayName  = "Cap w/DEF (New York)";
	descriptionShort = "$STR_A3_SP_NOARMOR";
	picture = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_PMC\data\ui\icon_h_pmc_cap_prr_tan_ca.paa";
	model   = "\A3\Characters_F\common\capb_headphones.p3d";
	hiddenSelections[] = {"camo"};
	hiddenSelectionsTextures[] = {"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\data\cap_def_ny_co.paa"};
	class ItemInfo: HeadgearItem
	{
		mass = 10;
		uniformModel = "\A3\Characters_F\common\capb_headphones.p3d";
		allowedSlots[] = {UNIFORM_SLOT, BACKPACK_SLOT, VEST_SLOT, HEADGEAR_SLOT};
		modelSides[] = {6};
		armor = 0;
		passThrough = 1;
		hiddenSelections[] = {"camo"};
		hiddenSelectionsTextures[] = {"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\data\cap_def_ny_co.paa"};
		#include "\CUP\Creatures\hitpoints_headno.h"
	};
	ace_hearing_protection = 0.75;
	ace_hearing_lowerVolume = 0.5;
};

class CUP_H_USA_Cap_PUNISHER_DEF: ItemCore
{
	CUP_HEADER_PUBLIC;
	displayName  = "Cap w/DEF (Punisher)";
	descriptionShort = "$STR_A3_SP_NOARMOR";
	picture = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_PMC\data\ui\icon_h_pmc_cap_prr_tan_ca.paa";
	model   = "\A3\Characters_F\common\capb_headphones.p3d";
	hiddenSelections[] = {"camo"};
	hiddenSelectionsTextures[] = {"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\data\cap_def_punisher_co.paa"};
	class ItemInfo: HeadgearItem
	{
		mass = 10;
		uniformModel = "\A3\Characters_F\common\capb_headphones.p3d";
		allowedSlots[] = {UNIFORM_SLOT, BACKPACK_SLOT, VEST_SLOT, HEADGEAR_SLOT};
		modelSides[] = {6};
		armor = 0;
		passThrough = 1;
		hiddenSelections[] = {"camo"};
		hiddenSelectionsTextures[] = {"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\data\cap_def_punisher_co.paa"};
		#include "\CUP\Creatures\hitpoints_headno.h"
	};
	ace_hearing_protection = 0.75;
	ace_hearing_lowerVolume = 0.5;
};

class CUP_H_USA_Cap_TREAD_DEF: ItemCore
{
	CUP_HEADER_PUBLIC;
	displayName  = "Cap w/DEF (Don't Tread on Me)";
	descriptionShort = "$STR_A3_SP_NOARMOR";
	picture = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_PMC\data\ui\icon_h_pmc_cap_prr_tan_ca.paa";
	model   = "\A3\Characters_F\common\capb_headphones.p3d";
	hiddenSelections[] = {"camo"};
	hiddenSelectionsTextures[] = {"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\data\cap_def_tread_co.paa"};
	class ItemInfo: HeadgearItem
	{
		mass = 10;
		uniformModel = "\A3\Characters_F\common\capb_headphones.p3d";
		allowedSlots[] = {UNIFORM_SLOT, BACKPACK_SLOT, VEST_SLOT, HEADGEAR_SLOT};
		modelSides[] = {6};
		armor = 0;
		passThrough = 1;
		hiddenSelections[] = {"camo"};
		hiddenSelectionsTextures[] = {"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\data\cap_def_tread_co.paa"};
		#include "\CUP\Creatures\hitpoints_headno.h"
	};
	ace_hearing_protection = 0.75;
	ace_hearing_lowerVolume = 0.5;
};

class CUP_H_USA_Cap_MARSOC_DEF: ItemCore
{
	CUP_HEADER_PUBLIC;
	displayName  = "Cap w/DEF (MARSOC Patch)";
	descriptionShort = "$STR_A3_SP_NOARMOR";
	picture = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_PMC\data\ui\icon_h_pmc_cap_prr_tan_ca.paa";
	model   = "\A3\Characters_F\common\capb_headphones.p3d";
	hiddenSelections[] = {"camo"};
	hiddenSelectionsTextures[] = {"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\data\cap_def_marsoc_co.paa"};
	class ItemInfo: HeadgearItem
	{
		mass = 10;
		uniformModel = "\A3\Characters_F\common\capb_headphones.p3d";
		allowedSlots[] = {UNIFORM_SLOT, BACKPACK_SLOT, VEST_SLOT, HEADGEAR_SLOT};
		modelSides[] = {6};
		armor = 0;
		passThrough = 1;
		hiddenSelections[] = {"camo"};
		hiddenSelectionsTextures[] = {"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\data\cap_def_marsoc_co.paa"};
		#include "\CUP\Creatures\hitpoints_headno.h"
	};
	ace_hearing_protection = 0.75;
	ace_hearing_lowerVolume = 0.5;
};

class CUP_H_USA_Cap_MCAM: ItemCore
{
	CUP_HEADER_PUBLIC;
	displayName  = "Cap (Multicam)";
	descriptionShort = "$STR_A3_SP_NOARMOR";
	picture = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_PMC\data\ui\icon_h_pmc_cap_tan_ca.paa";
	model   = "\A3\Characters_F\common\capb";
	hiddenSelections[] = {"camo"};
	hiddenSelectionsTextures[] = {"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\data\capb_mcam_co.paa"};
	class ItemInfo: HeadgearItem
	{
		mass = 10;
		uniformModel = "\A3\Characters_F\common\capb";
		allowedSlots[] = {UNIFORM_SLOT, BACKPACK_SLOT, VEST_SLOT, HEADGEAR_SLOT};
		modelSides[] = {6};
		armor = 0;
		passThrough = 1;
		hiddenSelections[] = {"camo"};
		hiddenSelectionsTextures[] = {"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\data\capb_mcam_co.paa"};
		#include "\CUP\Creatures\hitpoints_headno.h"
	};
};

class CUP_H_USA_Cap_M81: ItemCore
{
	CUP_HEADER_PUBLIC;
	displayName  = "Cap (M81)";
	descriptionShort = "$STR_A3_SP_NOARMOR";
	picture = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_PMC\data\ui\icon_h_pmc_cap_tan_ca.paa";
	model   = "\A3\Characters_F\common\capb";
	hiddenSelections[] = {"camo"};
	hiddenSelectionsTextures[] = {"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\data\capb_m81_co.paa"};
	class ItemInfo: HeadgearItem
	{
		mass = 10;
		uniformModel = "\A3\Characters_F\common\capb";
		allowedSlots[] = {UNIFORM_SLOT, BACKPACK_SLOT, VEST_SLOT, HEADGEAR_SLOT};
		modelSides[] = {6};
		armor = 0;
		passThrough = 1;
		hiddenSelections[] = {"camo"};
		hiddenSelectionsTextures[] = {"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\data\capb_m81_co.paa"};
		#include "\CUP\Creatures\hitpoints_headno.h"
	};
};

// MICH
class CUP_H_USArmy_HelmetMICH: ItemCore
{
	CUP_HEADER_PROTECTED;
	displayName  = "MICH 2000 (ACU)";
	descriptionShort = "$STR_A3_SP_AL_II";
	picture = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USMC\data\ui\icon_H_USMC_HelmetWDL_ca.paa";
	model   = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\CUP_h_usarmy_mich.p3d";
	hiddenSelections[] = {"Camo1"};
	hiddenSelectionsTextures[] = {"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USarmy\data\tex2_co.paa"};
	class ItemInfo: HeadgearItem
	{
		mass = 40;
		uniformModel = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\CUP_h_usarmy_mich.p3d";
		allowedSlots[] = {UNIFORM_SLOT, BACKPACK_SLOT, VEST_SLOT, HEADGEAR_SLOT};
		modelSides[] = {6};
		armor = 3;
		passThrough = 0.5;
		hiddenSelections[] = {"Camo1"};
		#include "\CUP\Creatures\hitpoints_headmid.h"
	};
};
class CUP_H_USArmy_HelmetMICH_DCU: ItemCore
{
	CUP_HEADER_PROTECTED;
	displayName  = "MICH 2000 (DCU)";
	descriptionShort = "$STR_A3_SP_AL_II";
	picture = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USMC\data\ui\icon_H_USMC_HelmetWDL_ca.paa";
	model   = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\CUP_h_usarmy_mich.p3d";
	hiddenSelections[] = {"Camo1"};
	hiddenSelectionsTextures[] = {"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USarmy\data\tex2_dcu_co.paa"};
	class ItemInfo: HeadgearItem
	{
		mass = 40;
		uniformModel = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\CUP_h_usarmy_mich.p3d";
		allowedSlots[] = {UNIFORM_SLOT, BACKPACK_SLOT, VEST_SLOT, HEADGEAR_SLOT};
		modelSides[] = {6};
		armor = 3;
		passThrough = 0.5;
		hiddenSelections[] = {"Camo1"};
		#include "\CUP\Creatures\hitpoints_headmid.h"
	};
};
class CUP_H_USArmy_HelmetMICH_ESS: ItemCore
{
	CUP_HEADER_PROTECTED;
	displayName  = "MICH 2000 (ACU - ESS)";
	descriptionShort = "$STR_A3_SP_AL_II";
	picture = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USMC\data\ui\icon_H_USMC_HelmetWDL_ca.paa";
	model   = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\CUP_h_usarmy_mich_gog.p3d";
	hiddenSelections[] = {"Camo1"};
	hiddenSelectionsTextures[] = {"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USarmy\data\tex2_co.paa"};
	class ItemInfo: HeadgearItem
	{
		mass = 40;
		uniformModel = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\CUP_h_usarmy_mich_gog.p3d";
		allowedSlots[] = {UNIFORM_SLOT, BACKPACK_SLOT, VEST_SLOT, HEADGEAR_SLOT};
		modelSides[] = {6};
		armor = 3;
		passThrough = 0.5;
		hiddenSelections[] = {"Camo1"};
		#include "\CUP\Creatures\hitpoints_headmid.h"
	};
};
class CUP_H_USArmy_HelmetMICH_ESS_DCU: ItemCore
{
	CUP_HEADER_PROTECTED;
	displayName  = "MICH 2000 (DCU - ESS)";
	descriptionShort = "$STR_A3_SP_AL_II";
	picture = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USMC\data\ui\icon_H_USMC_HelmetWDL_ca.paa";
	model   = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\CUP_h_usarmy_mich_gog.p3d";
	hiddenSelections[] = {"Camo1"};
	hiddenSelectionsTextures[] = {"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USarmy\data\tex2_dcu_co.paa"};
	class ItemInfo: HeadgearItem
	{
		mass = 40;
		uniformModel = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\CUP_h_usarmy_mich_gog.p3d";
		allowedSlots[] = {UNIFORM_SLOT, BACKPACK_SLOT, VEST_SLOT, HEADGEAR_SLOT};
		modelSides[] = {6};
		armor = 3;
		passThrough = 0.5;
		hiddenSelections[] = {"Camo1"};
		#include "\CUP\Creatures\hitpoints_headmid.h"
	};
};
class CUP_H_USArmy_HelmetMICH_ESS_wdl: ItemCore
{
	CUP_HEADER_PROTECTED;
	displayName  = "MICH 2000 (M81 - ESS)";
	descriptionShort = "$STR_A3_SP_AL_II";
	picture = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USMC\data\ui\icon_H_USMC_HelmetWDL_ca.paa";
	model   = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\CUP_h_usarmy_mich_gog.p3d";
	hiddenSelections[] = {"Camo1"};
	hiddenSelectionsTextures[] = {"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USarmy\data\mich_m81_co.paa"};
	class ItemInfo: HeadgearItem
	{
		mass = 40;
		uniformModel = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\CUP_h_usarmy_mich_gog.p3d";
		allowedSlots[] = {UNIFORM_SLOT, BACKPACK_SLOT, VEST_SLOT, HEADGEAR_SLOT};
		modelSides[] = {6};
		armor = 3;
		passThrough = 0.5;
		hiddenSelections[] = {"Camo1"};
		#include "\CUP\Creatures\hitpoints_headmid.h"
	};
};
class CUP_H_USArmy_HelmetMICH_earpro: ItemCore
{
	CUP_HEADER_PROTECTED;
	displayName  = "MICH 2000 (ACU - Ear Pro)";
	descriptionShort = "$STR_A3_SP_AL_II";
	picture = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USMC\data\ui\icon_H_USMC_HelmetWDL_ca.paa";
	model   = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\CUP_h_usarmy_mich_ear.p3d";
	hiddenSelections[] = {"Camo1"};
	hiddenSelectionsTextures[] = {"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USarmy\data\tex2_co.paa"};
	class ItemInfo: HeadgearItem
	{
		mass = 40;
		uniformModel = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\CUP_h_usarmy_mich_ear.p3d";
		allowedSlots[] = {UNIFORM_SLOT, BACKPACK_SLOT, VEST_SLOT, HEADGEAR_SLOT};
		modelSides[] = {6};
		armor = 3;
		passThrough = 0.5;
		hiddenSelections[] = {"Camo1"};
		#include "\CUP\Creatures\hitpoints_headmid.h"
	};
	ace_hearing_protection = 0.75;
};
class CUP_H_USArmy_HelmetMICH_earpro_DCU: ItemCore
{
	CUP_HEADER_PROTECTED;
	displayName  = "MICH 2000 (DCU - Ear Pro)";
	descriptionShort = "$STR_A3_SP_AL_II";
	picture = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USMC\data\ui\icon_H_USMC_HelmetWDL_ca.paa";
	model   = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\CUP_h_usarmy_mich_ear.p3d";
	hiddenSelections[] = {"Camo1"};
	hiddenSelectionsTextures[] = {"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USarmy\data\tex2_dcu_co.paa"};
	class ItemInfo: HeadgearItem
	{
		mass = 40;
		uniformModel = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\CUP_h_usarmy_mich_ear.p3d";
		allowedSlots[] = {UNIFORM_SLOT, BACKPACK_SLOT, VEST_SLOT, HEADGEAR_SLOT};
		modelSides[] = {6};
		armor = 3;
		passThrough = 0.5;
		hiddenSelections[] = {"Camo1"};
		#include "\CUP\Creatures\hitpoints_headmid.h"
	};
	ace_hearing_protection = 0.75;
};
class CUP_H_USArmy_HelmetMICH_earpro_wdl: ItemCore
{
	CUP_HEADER_PROTECTED;
	displayName  = "MICH 2000 (M81 - Ear Pro)";
	descriptionShort = "$STR_A3_SP_AL_II";
	picture = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USMC\data\ui\icon_H_USMC_HelmetWDL_ca.paa";
	model   = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\CUP_h_usarmy_mich_ear.p3d";
	hiddenSelections[] = {"Camo1"};
	hiddenSelectionsTextures[] = {"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USarmy\data\mich_m81_co.paa"};
	class ItemInfo: HeadgearItem
	{
		mass = 40;
		uniformModel = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\CUP_h_usarmy_mich_ear.p3d";
		allowedSlots[] = {UNIFORM_SLOT, BACKPACK_SLOT, VEST_SLOT, HEADGEAR_SLOT};
		modelSides[] = {6};
		armor = 3;
		passThrough = 0.5;
		hiddenSelections[] = {"Camo1"};
		#include "\CUP\Creatures\hitpoints_headmid.h"
	};
	ace_hearing_protection = 0.75;
};
class CUP_H_USArmy_HelmetMICH_earpro_ess: ItemCore
{
	CUP_HEADER_PROTECTED;
	displayName  = "MICH 2000 (ACU - Ear Pro - ESS)";
	descriptionShort = "$STR_A3_SP_AL_II";
	picture = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USMC\data\ui\icon_H_USMC_HelmetWDL_ca.paa";
	model   = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\CUP_h_usarmy_mich_ear_gog.p3d";
	hiddenSelections[] = {"Camo1"};
	hiddenSelectionsTextures[] = {"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USarmy\data\tex2_co.paa"};
	class ItemInfo: HeadgearItem
	{
		mass = 40;
		uniformModel = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\CUP_h_usarmy_mich_ear_gog.p3d";
		allowedSlots[] = {UNIFORM_SLOT, BACKPACK_SLOT, VEST_SLOT, HEADGEAR_SLOT};
		modelSides[] = {6};
		armor = 3;
		passThrough = 0.5;
		hiddenSelections[] = {"Camo1"};
		#include "\CUP\Creatures\hitpoints_headmid.h"
	};
	ace_hearing_protection = 0.75;
};
class CUP_H_USArmy_HelmetMICH_earpro_ess_DCU: ItemCore
{
	CUP_HEADER_PROTECTED;
	displayName  = "MICH 2000 (DCU - Ear Pro - ESS)";
	descriptionShort = "$STR_A3_SP_AL_II";
	picture = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USMC\data\ui\icon_H_USMC_HelmetWDL_ca.paa";
	model   = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\CUP_h_usarmy_mich_ear_gog.p3d";
	hiddenSelections[] = {"Camo1"};
	hiddenSelectionsTextures[] = {"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USarmy\data\tex2_dcu_co.paa"};
	class ItemInfo: HeadgearItem
	{
		mass = 40;
		uniformModel = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\CUP_h_usarmy_mich_ear_gog.p3d";
		allowedSlots[] = {UNIFORM_SLOT, BACKPACK_SLOT, VEST_SLOT, HEADGEAR_SLOT};
		modelSides[] = {6};
		armor = 3;
		passThrough = 0.5;
		hiddenSelections[] = {"Camo1"};
		#include "\CUP\Creatures\hitpoints_headmid.h"
	};
	ace_hearing_protection = 0.75;
};
class CUP_H_USArmy_HelmetMICH_earpro_ess_wdl: ItemCore
{
	CUP_HEADER_PROTECTED;
	displayName  = "MICH 2000 (M81 - Ear Pro - ESS)";
	descriptionShort = "$STR_A3_SP_AL_II";
	picture = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USMC\data\ui\icon_H_USMC_HelmetWDL_ca.paa";
	model   = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\CUP_h_usarmy_mich_ear_gog.p3d";
	hiddenSelections[] = {"Camo1"};
	hiddenSelectionsTextures[] = {"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USarmy\data\mich_m81_co.paa"};
	class ItemInfo: HeadgearItem
	{
		mass = 40;
		uniformModel = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\CUP_h_usarmy_mich_ear_gog.p3d";
		allowedSlots[] = {UNIFORM_SLOT, BACKPACK_SLOT, VEST_SLOT, HEADGEAR_SLOT};
		modelSides[] = {6};
		armor = 3;
		passThrough = 0.5;
		hiddenSelections[] = {"Camo1"};
		#include "\CUP\Creatures\hitpoints_headmid.h"
	};
	ace_hearing_protection = 0.75;
};
class CUP_H_USArmy_HelmetMICH_headset: ItemCore
{
	CUP_HEADER_PROTECTED;
	displayName  = "MICH 2000 (ACU - Headset)";
	descriptionShort = "$STR_A3_SP_AL_II";
	picture = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USMC\data\ui\icon_H_USMC_HelmetWDL_ca.paa";
	model   = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\CUP_h_usarmy_mich_headset.p3d";
	hiddenSelections[] = {"Camo1"};
	hiddenSelectionsTextures[] = {"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USarmy\data\tex2_co.paa"};
	class ItemInfo: HeadgearItem
	{
		mass = 40;
		uniformModel = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\CUP_h_usarmy_mich_headset.p3d";
		allowedSlots[] = {UNIFORM_SLOT, BACKPACK_SLOT, VEST_SLOT, HEADGEAR_SLOT};
		modelSides[] = {6};
		armor = 3;
		passThrough = 0.5;
		hiddenSelections[] = {"Camo1"};
		#include "\CUP\Creatures\hitpoints_headmid.h"
	};
};
class CUP_H_USArmy_HelmetMICH_headset_DCU: ItemCore
{
	CUP_HEADER_PROTECTED;
	displayName  = "MICH 2000 (DCU - Headset)";
	descriptionShort = "$STR_A3_SP_AL_II";
	picture = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USMC\data\ui\icon_H_USMC_HelmetWDL_ca.paa";
	model   = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\CUP_h_usarmy_mich_headset.p3d";
	hiddenSelections[] = {"Camo1"};
	hiddenSelectionsTextures[] = {"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USarmy\data\tex2_dcu_co.paa"};
	class ItemInfo: HeadgearItem
	{
		mass = 40;
		uniformModel = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\CUP_h_usarmy_mich_headset.p3d";
		allowedSlots[] = {UNIFORM_SLOT, BACKPACK_SLOT, VEST_SLOT, HEADGEAR_SLOT};
		modelSides[] = {6};
		armor = 3;
		passThrough = 0.5;
		hiddenSelections[] = {"Camo1"};
		#include "\CUP\Creatures\hitpoints_headmid.h"
	};
};
class CUP_H_USArmy_HelmetMICH_headset_wdl: ItemCore
{
	CUP_HEADER_PROTECTED;
	displayName  = "MICH 2000 (M81 - Headset)";
	descriptionShort = "$STR_A3_SP_AL_II";
	picture = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USMC\data\ui\icon_H_USMC_HelmetWDL_ca.paa";
	model   = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\CUP_h_usarmy_mich_headset.p3d";
	hiddenSelections[] = {"Camo1"};
	hiddenSelectionsTextures[] = {"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USarmy\data\mich_m81_co.paa"};
	class ItemInfo: HeadgearItem
	{
		mass = 40;
		uniformModel = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\CUP_h_usarmy_mich_headset.p3d";
		allowedSlots[] = {UNIFORM_SLOT, BACKPACK_SLOT, VEST_SLOT, HEADGEAR_SLOT};
		modelSides[] = {6};
		armor = 3;
		passThrough = 0.5;
		hiddenSelections[] = {"Camo1"};
		#include "\CUP\Creatures\hitpoints_headmid.h"
	};
};
class CUP_H_USArmy_HelmetMICH_headset_ess: ItemCore
{
	CUP_HEADER_PROTECTED;
	displayName  = "MICH 2000 (ACU - Headset - ESS)";
	descriptionShort = "$STR_A3_SP_AL_II";
	picture = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USMC\data\ui\icon_H_USMC_HelmetWDL_ca.paa";
	model   = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\CUP_h_usarmy_mich_headset_gog.p3d";
	hiddenSelections[] = {"Camo1"};
	hiddenSelectionsTextures[] = {"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USarmy\data\tex2_co.paa"};
	class ItemInfo: HeadgearItem
	{
		mass = 40;
		uniformModel = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\CUP_h_usarmy_mich_headset_gog.p3d";
		allowedSlots[] = {UNIFORM_SLOT, BACKPACK_SLOT, VEST_SLOT, HEADGEAR_SLOT};
		modelSides[] = {6};
		armor = 3;
		passThrough = 0.5;
		hiddenSelections[] = {"Camo1"};
		#include "\CUP\Creatures\hitpoints_headmid.h"
	};
};
class CUP_H_USArmy_HelmetMICH_headset_ess_DCU: ItemCore
{
	CUP_HEADER_PROTECTED;
	displayName  = "MICH 2000 (DCU - Headset - ESS)";
	descriptionShort = "$STR_A3_SP_AL_II";
	picture = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USMC\data\ui\icon_H_USMC_HelmetWDL_ca.paa";
	model   = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\CUP_h_usarmy_mich_headset_gog.p3d";
	hiddenSelections[] = {"Camo1"};
	hiddenSelectionsTextures[] = {"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USarmy\data\tex2_dcu_co.paa"};
	class ItemInfo: HeadgearItem
	{
		mass = 40;
		uniformModel = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\CUP_h_usarmy_mich_headset_gog.p3d";
		allowedSlots[] = {UNIFORM_SLOT, BACKPACK_SLOT, VEST_SLOT, HEADGEAR_SLOT};
		modelSides[] = {6};
		armor = 3;
		passThrough = 0.5;
		hiddenSelections[] = {"Camo1"};
		#include "\CUP\Creatures\hitpoints_headmid.h"
	};
};
class CUP_H_USArmy_HelmetMICH_wdl: ItemCore
{
	CUP_HEADER_PROTECTED;
	displayName  = "MICH 2000 (M81)";
	descriptionShort = "$STR_A3_SP_AL_II";
	picture = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USMC\data\ui\icon_H_USMC_HelmetWDL_ca.paa";
	model   = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\CUP_h_usarmy_mich.p3d";
	hiddenSelections[] = {"Camo1"};
	hiddenSelectionsTextures[] = {"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USarmy\data\mich_m81_co.paa"};
	class ItemInfo: HeadgearItem
	{
		mass = 40;
		uniformModel = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\CUP_h_usarmy_mich.p3d";
		allowedSlots[] = {UNIFORM_SLOT, BACKPACK_SLOT, VEST_SLOT, HEADGEAR_SLOT};
		modelSides[] = {6};
		armor = 3;
		passThrough = 0.5;
		hiddenSelections[] = {"Camo1"};
		#include "\CUP\Creatures\hitpoints_headmid.h"
	};
};

// ECH
class CUP_H_USArmy_Helmet_ECH1_Sand: ItemCore
{
	CUP_HEADER_PUBLIC;
	displayName  = "ECH (Sand)";
	descriptionShort = "$STR_A3_SP_AL_II";
	picture = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USMC\data\ui\icon_H_USMC_HelmetWDL_ca.paa";
	model   = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\CUP_h_delta_ech1.p3d";
	hiddenSelections[] = {"Camo"};
	hiddenSelectionsTextures[] = {"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USarmy\data\delta\do_helmets_co.paa"};
	class ItemInfo: HeadgearItem
	{
		mass = 40;
		uniformModel = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\CUP_h_delta_ech1.p3d";
		allowedSlots[] = {UNIFORM_SLOT, BACKPACK_SLOT, VEST_SLOT, HEADGEAR_SLOT};
		modelSides[] = {6};
		armor = 3;
		passThrough = 0.5;
		hiddenSelections[] = {"Camo1"};
		#include "\CUP\Creatures\hitpoints_headmid.h"
	};
	ace_hearing_protection = 0.75;
};
class CUP_H_USArmy_Helmet_ECH2_Sand: ItemCore
{
	CUP_HEADER_PUBLIC;
	displayName  = "ECH (Sand - ESS)";
	descriptionShort = "$STR_A3_SP_AL_II";
	picture = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USMC\data\ui\icon_H_USMC_HelmetWDL_ca.paa";
	model   = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\CUP_h_delta_ech2.p3d";
	hiddenSelections[] = {"Camo", "Camo2"};
	hiddenSelectionsTextures[] = {"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USarmy\data\delta\do_helmets_co.paa", "cup\creatures\people\military\cup_creatures_people_military_usarmy\data\delta\do_equip_co.paa"};
	class ItemInfo: HeadgearItem
	{
		mass = 40;
		uniformModel = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\CUP_h_delta_ech2.p3d";
		allowedSlots[] = {UNIFORM_SLOT, BACKPACK_SLOT, VEST_SLOT, HEADGEAR_SLOT};
		modelSides[] = {6};
		armor = 3;
		passThrough = 0.5;
		hiddenSelections[] = {"Camo1"};
		#include "\CUP\Creatures\hitpoints_headmid.h"
	};
	ace_hearing_protection = 0.75;
};
class CUP_H_USArmy_Helmet_ECH1_Black: ItemCore
{
	CUP_HEADER_PUBLIC;
	displayName  = "ECH (Black)";
	descriptionShort = "$STR_A3_SP_AL_II";
	picture = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USMC\data\ui\icon_H_USMC_HelmetWDL_ca.paa";
	model   = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\CUP_h_delta_ech1.p3d";
	hiddenSelections[] = {"Camo"};
	hiddenSelectionsTextures[] = {"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USarmy\data\delta\do_helmets_black_co.paa"};
	class ItemInfo: HeadgearItem
	{
		mass = 40;
		uniformModel = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\CUP_h_delta_ech1.p3d";
		allowedSlots[] = {UNIFORM_SLOT, BACKPACK_SLOT, VEST_SLOT, HEADGEAR_SLOT};
		modelSides[] = {6};
		armor = 3;
		passThrough = 0.5;
		hiddenSelections[] = {"Camo"};
		#include "\CUP\Creatures\hitpoints_headmid.h"
	};
	ace_hearing_protection = 0.75;
};
class CUP_H_USArmy_Helmet_ECH2_Black: ItemCore
{
	CUP_HEADER_PUBLIC;
	displayName  = "ECH (Black - ESS)";
	descriptionShort = "$STR_A3_SP_AL_II";
	picture = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USMC\data\ui\icon_H_USMC_HelmetWDL_ca.paa";
	model   = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\CUP_h_delta_ech2.p3d";
	hiddenSelections[] = {"Camo", "Camo2"};
	hiddenSelectionsTextures[] = {"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USarmy\data\delta\do_helmets_black_co.paa", "cup\creatures\people\military\cup_creatures_people_military_usarmy\data\delta\do_equip_co.paa"};
	class ItemInfo: HeadgearItem
	{
		mass = 40;
		uniformModel = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\CUP_h_delta_ech2.p3d";
		allowedSlots[] = {UNIFORM_SLOT, BACKPACK_SLOT, VEST_SLOT, HEADGEAR_SLOT};
		modelSides[] = {6};
		armor = 3;
		passThrough = 0.5;
		hiddenSelections[] = {"Camo", "Camo2"};
		#include "\CUP\Creatures\hitpoints_headmid.h"
	};
	ace_hearing_protection = 0.75;
};
class CUP_H_USArmy_Helmet_ECH1_Green: ItemCore
{
	CUP_HEADER_PUBLIC;
	displayName  = "ECH (Green)";
	descriptionShort = "$STR_A3_SP_AL_II";
	picture = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USMC\data\ui\icon_H_USMC_HelmetWDL_ca.paa";
	model   = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\CUP_h_delta_ech1.p3d";
	hiddenSelections[] = {"Camo"};
	hiddenSelectionsTextures[] = {"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USarmy\data\delta\do_helmets_green_co.paa"};
	class ItemInfo: HeadgearItem
	{
		mass = 40;
		uniformModel = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\CUP_h_delta_ech1.p3d";
		allowedSlots[] = {UNIFORM_SLOT, BACKPACK_SLOT, VEST_SLOT, HEADGEAR_SLOT};
		modelSides[] = {6};
		armor = 3;
		passThrough = 0.5;
		hiddenSelections[] = {"Camo"};
		#include "\CUP\Creatures\hitpoints_headmid.h"
	};
	ace_hearing_protection = 0.75;
};
class CUP_H_USArmy_Helmet_ECH2_GREEN: ItemCore
{
	CUP_HEADER_PUBLIC;
	displayName  = "ECH (Green - ESS)";
	descriptionShort = "$STR_A3_SP_AL_II";
	picture = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USMC\data\ui\icon_H_USMC_HelmetWDL_ca.paa";
	model   = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\CUP_h_delta_ech2.p3d";
	hiddenSelections[] = {"Camo", "Camo2"};
	hiddenSelectionsTextures[] = {"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USarmy\data\delta\do_helmets_green_co.paa", "cup\creatures\people\military\cup_creatures_people_military_usarmy\data\delta\do_equip_co.paa"};
	class ItemInfo: HeadgearItem
	{
		mass = 40;
		uniformModel = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\CUP_h_delta_ech2.p3d";
		allowedSlots[] = {UNIFORM_SLOT, BACKPACK_SLOT, VEST_SLOT, HEADGEAR_SLOT};
		modelSides[] = {6};
		armor = 3;
		passThrough = 0.5;
		hiddenSelections[] = {"Camo", "Camo2"};
		#include "\CUP\Creatures\hitpoints_headmid.h"
	};
	ace_hearing_protection = 0.75;
};

// Protec Helmet
class CUP_H_USArmy_Helmet_Protec: ItemCore
{
	CUP_HEADER_PUBLIC;
	displayName  = "Pro-Tec";
	descriptionShort = "$STR_A3_SP_AL_I";
	picture = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USMC\data\ui\icon_H_USMC_HelmetWDL_ca.paa";
	model   = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\CUP_h_protec.p3d";
	hiddenSelections[] = {"Camo"};
	hiddenSelectionsTextures[] = {"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USarmy\data\protec\protec_base_co.paa"};
	class ItemInfo: HeadgearItem
	{
		mass = 40;
		uniformModel = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\CUP_h_protec.p3d";
		allowedSlots[] = {UNIFORM_SLOT, BACKPACK_SLOT, VEST_SLOT, HEADGEAR_SLOT};
		modelSides[] = {6};
		armor = 3;
		passThrough = 0.5;
		hiddenSelections[] = {"Camo"};
		#include "\CUP\Creatures\hitpoints_headno.h"
	};
};
class CUP_H_USArmy_Helmet_Protec_Gog: ItemCore
{
	CUP_HEADER_PUBLIC;
	displayName  = "Pro-Tec (Goggles)";
	descriptionShort = "$STR_A3_SP_AL_I";
	picture = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USMC\data\ui\icon_H_USMC_HelmetWDL_ca.paa";
	model   = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\CUP_h_protec_gog.p3d";
	hiddenSelections[] = {"Camo"};
	hiddenSelectionsTextures[] = {"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USarmy\data\protec\protec_base_co.paa"};
	class ItemInfo: HeadgearItem
	{
		mass = 40;
		uniformModel = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\CUP_h_protec_gog.p3d";
		allowedSlots[] = {UNIFORM_SLOT, BACKPACK_SLOT, VEST_SLOT, HEADGEAR_SLOT};
		modelSides[] = {6};
		armor = 3;
		passThrough = 0.5;
		hiddenSelections[] = {"Camo"};
		#include "\CUP\Creatures\hitpoints_headno.h"
	};
};
class CUP_H_USArmy_Helmet_Protec_Gog_Strb: ItemCore
{
	dlc = "CUP_Units";
	scope = 2;
	author = "Community Upgrade Project";
	displayName  = "Pro-Tec (Goggles/Strobe)";
	descriptionShort = "$STR_A3_SP_AL_I";
	picture = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USMC\data\ui\icon_H_USMC_HelmetWDL_ca.paa";
	model   = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\CUP_h_protec_gog_strb.p3d";
	hiddenSelections[] = {"Camo"};
	hiddenSelectionsTextures[] = {"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USarmy\data\protec\protec_base_co.paa"};
	class ItemInfo: HeadgearItem
	{
		mass = 40;
		uniformModel = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\CUP_h_protec_gog_strb.p3d";
		allowedSlots[] = {UNIFORM_SLOT, BACKPACK_SLOT, VEST_SLOT, HEADGEAR_SLOT};
		modelSides[] = {6};
		armor = 3;
		passThrough = 0.5;
		hiddenSelections[] = {"Camo"};
		#include "\CUP\Creatures\hitpoints_headno.h"
	};
};
class CUP_H_USArmy_Helmet_Protec_NVG: ItemCore
{
	dlc = "CUP_Units";
	scope = 2;
	author = "Community Upgrade Project";
	displayName  = "Pro-Tec (NVG)";
	descriptionShort = "$STR_A3_SP_AL_I";
	picture = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USMC\data\ui\icon_H_USMC_HelmetWDL_ca.paa";
	model   = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\CUP_h_protec_nvg.p3d";
	hiddenSelections[] = {"Camo"};
	hiddenSelectionsTextures[] = {"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USarmy\data\protec\protec_base_co.paa"};
	class ItemInfo: HeadgearItem
	{
		mass = 40;
		uniformModel = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\CUP_h_protec_nvg.p3d";
		allowedSlots[] = {UNIFORM_SLOT, BACKPACK_SLOT, VEST_SLOT, HEADGEAR_SLOT};
		modelSides[] = {6};
		armor = 3;
		passThrough = 0.5;
		hiddenSelections[] = {"Camo"};
		#include "\CUP\Creatures\hitpoints_headno.h"
	};
};
//legacy classes
class CUP_H_USArmy_Helmet_Pro: CUP_H_USArmy_Helmet_Protec{scope=1;};
class CUP_H_USArmy_Helmet_Pro_gog: CUP_H_USArmy_Helmet_Protec_Gog{scope=1;};

// M1 Helmet
class CUP_H_USArmy_Helmet_M1_Olive: ItemCore
{
	CUP_HEADER_PUBLIC;
	displayName  = "M1 (Cigs/Olive)";
	descriptionShort = "$STR_A3_SP_AL_II";
	picture = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USarmy\data\ui\gear_h_b_m1_olive_ca.paa";
	model   = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\CUP_h_m1.p3d";
	hiddenSelections[] = {"Camo"};
	hiddenSelectionsTextures[] = {"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USarmy\data\m1\merc_g_co.paa"};
	class ItemInfo: HeadgearItem
	{
		mass = 40;
		uniformModel = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\CUP_h_m1.p3d";
		allowedSlots[] = {UNIFORM_SLOT, BACKPACK_SLOT, VEST_SLOT, HEADGEAR_SLOT};
		modelSides[] = {6};
		armor = 3;
		passThrough = 0.5;
		hiddenSelections[] = {"Camo"};
		#include "\CUP\Creatures\hitpoints_headlight.h"
	};
};
class CUP_H_USArmy_Helmet_M1_Vine: ItemCore
{
	CUP_HEADER_PUBLIC;
	displayName  = "M1 (Cigs/Leaf)";
	descriptionShort = "$STR_A3_SP_AL_II";
	picture = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USarmy\data\ui\gear_h_b_m1_vineleaf_ca.paa";
	model   = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\CUP_h_m1.p3d";
	hiddenSelections[] = {"Camo"};
	hiddenSelectionsTextures[] = {"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USarmy\data\m1\merc_g_vine_co.paa"};
	class ItemInfo: HeadgearItem
	{
		mass = 40;
		uniformModel = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\CUP_h_m1.p3d";
		allowedSlots[] = {UNIFORM_SLOT, BACKPACK_SLOT, VEST_SLOT, HEADGEAR_SLOT};
		modelSides[] = {6};
		armor = 3;
		passThrough = 0.5;
		hiddenSelections[] = {"Camo"};
		#include "\CUP\Creatures\hitpoints_headlight.h"
	};
};
class CUP_H_USArmy_Helmet_M1_m81: ItemCore
{
	CUP_HEADER_PUBLIC;
	displayName  = "M1 (Cigs/Woodland)";
	descriptionShort = "$STR_A3_SP_AL_II";
	picture = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USarmy\data\ui\gear_h_b_m1_m81_ca.paa";
	model   = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\CUP_h_m1.p3d";
	hiddenSelections[] = {"Camo"};
	hiddenSelectionsTextures[] = {"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USarmy\data\m1\merc_g_m81_co.paa"};
	class ItemInfo: HeadgearItem
	{
		mass = 40;
		uniformModel = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\CUP_h_m1.p3d";
		allowedSlots[] = {UNIFORM_SLOT, BACKPACK_SLOT, VEST_SLOT, HEADGEAR_SLOT};
		modelSides[] = {6};
		armor = 3;
		passThrough = 0.5;
		hiddenSelections[] = {"Camo"};
		#include "\CUP\Creatures\hitpoints_headlight.h"
	};
};
class CUP_H_USArmy_Helmet_M1_btp: ItemCore
{
	CUP_HEADER_PUBLIC;
	displayName  = "M1 (Cigs/CUP)";
	descriptionShort = "$STR_A3_SP_AL_II";
	picture = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USarmy\data\ui\gear_h_b_m1_vineleaf_ca.paa";
	model   = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\CUP_h_m1.p3d";
	hiddenSelections[] = {"Camo"};
	hiddenSelectionsTextures[] = {"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USarmy\data\m1\merc_g_vine_btp_co.paa"};
	class ItemInfo: HeadgearItem
	{
		mass = 40;
		uniformModel = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\CUP_h_m1.p3d";
		allowedSlots[] = {UNIFORM_SLOT, BACKPACK_SLOT, VEST_SLOT, HEADGEAR_SLOT};
		modelSides[] = {6};
		armor = 3;
		passThrough = 0.5;
		hiddenSelections[] = {"Camo"};
		#include "\CUP\Creatures\hitpoints_headlight.h"
	};
};

class CUP_H_USArmy_Helmet_M1_plain_Olive: ItemCore
{
	CUP_HEADER_PUBLIC;
	model="\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\cup_h_M1_plain.p3d";
	displayName  = "M1 (Olive)";
	picture = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USarmy\data\ui\gear_h_b_m1_olive_ca.paa";
	hiddenSelections[] = {"camo"};
	hiddenSelectionsTextures[] = {"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USarmy\data\m1\m1_plain_olive_co.paa"};
	class ItemInfo: HeadgearItem
	{
		mass = 40;
		uniformModel = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\CUP_h_m1_plain.p3d";
		hiddenSelections[] = {"camo"};
		hiddenSelectionsTextures[] = {"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USarmy\data\m1\m1_plain_olive_co.paa"};
		allowedSlots[] = {UNIFORM_SLOT, BACKPACK_SLOT, VEST_SLOT, HEADGEAR_SLOT};
		modelSides[] = {6};
		armor = 3;
		passThrough = 0.5;
		#include "\CUP\Creatures\hitpoints_headlight.h"
	};
};
class CUP_H_USArmy_Helmet_M1_plain_Vine: ItemCore
{
	CUP_HEADER_PUBLIC;
	model="\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\cup_h_M1_plain.p3d";
	displayName  = "M1 (Vineleaf)";
	picture = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USarmy\data\ui\gear_h_b_m1_vineleaf_ca.paa";
	hiddenSelections[] = {"camo"};
	hiddenSelectionsTextures[] = {"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USarmy\data\m1\m1_plain_vineleaf_co.paa"};
	class ItemInfo: HeadgearItem
	{
		mass = 40;
		uniformModel = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\CUP_h_m1_plain.p3d";
		hiddenSelections[] = {"camo"};
		hiddenSelectionsTextures[] = {"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USarmy\data\m1\m1_plain_vineleaf_co.paa"};
		allowedSlots[] = {UNIFORM_SLOT, BACKPACK_SLOT, VEST_SLOT, HEADGEAR_SLOT};
		modelSides[] = {6};
		armor = 3;
		passThrough = 0.5;
		#include "\CUP\Creatures\hitpoints_headlight.h"
	};
};
class CUP_H_USArmy_Helmet_M1_plain_M81: ItemCore
{
	CUP_HEADER_PUBLIC;
	model="\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\cup_h_M1_plain.p3d";
	displayName  = "M1 (Woodland M81)";
	picture = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USarmy\data\ui\gear_h_b_m1_m81_ca.paa";
	hiddenSelections[] = {"camo"};
	hiddenSelectionsTextures[] = {"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USarmy\data\m1\m1_plain_m81_co.paa"};
	class ItemInfo: HeadgearItem
	{
		mass = 40;
		uniformModel = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\CUP_h_m1_plain.p3d";
		hiddenSelections[] = {"camo"};
		hiddenSelectionsTextures[] = {"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USarmy\data\m1\m1_plain_m81_co.paa"};
		allowedSlots[] = {UNIFORM_SLOT, BACKPACK_SLOT, VEST_SLOT, HEADGEAR_SLOT};
		modelSides[] = {6};
		armor = 3;
		passThrough = 0.5;
		#include "\CUP\Creatures\hitpoints_headlight.h"
	};
};
// PASGTv2

class CUP_H_PASGTv2_WDL: ItemCore
{
	CUP_HEADER_PUBLIC;
	displayName  = "PASGT Helmet (M81 Woodland)";
	descriptionShort = "$STR_A3_SP_AL_II";
	picture = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USMC\data\ui\icon_H_USMC_HelmetWDL_ca.paa";
	uniformModel = "\cup\creatures\people\military\cup_creatures_people_military_usarmy\CUP_H_PASGTv2.p3d";
	hiddenSelections[] = {"camo", "NVG_mount", "Goggle_Glass", "Goggle_ESS", "Cover_Front", "Cover_Back"};
	hiddenSelectionsTextures[] = {
		"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\data\CUP_H_PASGT_CO.paa"
	};
	class ItemInfo: HeadgearItem
	{
		mass = 40;
		uniformModel = "\cup\creatures\people\military\cup_creatures_people_military_usarmy\CUP_H_PASGTv2.p3d";
		allowedSlots[] = {UNIFORM_SLOT, BACKPACK_SLOT, VEST_SLOT, HEADGEAR_SLOT};
		modelSides[] = {6};
		armor = 3;
		passThrough = 0.5;

		hiddenSelections[] = {"camo", "NVG_mount", "Goggle_Glass", "Goggle_ESS", "Cover_Front", "Cover_Back"};
		hiddenSelectionsTextures[] = {
			"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\data\CUP_H_PASGT_CO.paa"
		};
		#include "\CUP\Creatures\hitpoints_headmid.h"
	};
};
class CUP_H_PASGTv2_NVG_WDL: CUP_H_PASGTv2_WDL
{
	CUP_HEADER;
	displayName  = "PASGT Helmet (NVG, M81 Woodland)";
	hiddenSelections[] = {"camo", "NVG_mount", "Goggle_Glass", "Goggle_ESS", "Cover_Front", "Cover_Back"};
	hiddenSelectionsTextures[] = {
		"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\data\CUP_H_PASGT_CO.paa",
		"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USMC\data\new_usmc_gear3_tan_co.paa"
	};
	class ItemInfo: ItemInfo
	{
		hiddenSelections[] = {"camo", "NVG_mount", "Goggle_Glass", "Goggle_ESS", "Cover_Front", "Cover_Back"};
		hiddenSelectionsTextures[] = {
			"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\data\CUP_H_PASGT_CO.paa",
			"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USMC\data\new_usmc_gear3_tan_co.paa"
		};
	};
};
class CUP_H_PASGTv2_NVG_WDL_GG: CUP_H_PASGTv2_WDL
{
	CUP_HEADER;
	displayName  = "PASGT Helmet (NVG Goggles, M81 Woodland)";
	hiddenSelections[] = {"camo", "NVG_mount", "Goggle_Glass", "Goggle_ESS", "Cover_Front", "Cover_Back"};
	hiddenSelectionsTextures[] = {
		"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\data\CUP_H_PASGT_CO.paa",
		"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USMC\data\new_usmc_gear3_tan_co.paa"
	};
	class ItemInfo: ItemInfo
	{
		hiddenSelections[] = {"camo", "NVG_mount", "Cover_Front", "Cover_Back"};
		hiddenSelectionsTextures[] = {
			"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\data\CUP_H_PASGT_CO.paa",
			"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USMC\data\new_usmc_gear3_tan_co.paa"
		};
	};
};
class CUP_H_PASGTv2_NVG_WDL_CF: CUP_H_PASGTv2_WDL
{
	CUP_HEADER;
	displayName  = "PASGT Helmet (NVG Front Cover, M81 Woodland)";
	hiddenSelections[] = {"camo", "NVG_mount", "Goggle_Glass", "Goggle_ESS", "Cover_Front", "Cover_Back"};
	hiddenSelectionsTextures[] = {
		"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\data\CUP_H_PASGT_CO.paa",
		"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USMC\data\new_usmc_gear3_tan_co.paa"
	};
	class ItemInfo: ItemInfo
	{
		hiddenSelections[] = {"camo", "NVG_mount", "Goggle_Glass", "Cover_Back"};
		hiddenSelectionsTextures[] = {
			"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\data\CUP_H_PASGT_CO.paa",
			"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USMC\data\new_usmc_gear3_tan_co.paa"
		};
	};
};
class CUP_H_PASGTv2_NVG_WDL_GG_CB: CUP_H_PASGTv2_WDL
{
	CUP_HEADER;
	displayName  = "PASGT Helmet (NVG Goggles Back Cover, M81 Woodland)";
	hiddenSelections[] = {"camo", "NVG_mount", "Goggle_Glass", "Goggle_ESS", "Cover_Front", "Cover_Back"};
	hiddenSelectionsTextures[] = {
		"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\data\CUP_H_PASGT_CO.paa",
		"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USMC\data\new_usmc_gear3_tan_co.paa"
	};
	class ItemInfo: ItemInfo
	{
		hiddenSelections[] = {"camo", "NVG_mount", "Cover_Front"};
		hiddenSelectionsTextures[] = {
			"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\data\CUP_H_PASGT_CO.paa",
			"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USMC\data\new_usmc_gear3_tan_co.paa"
		};
	};
};
class CUP_H_PASGTv2_WDL_CF: CUP_H_PASGTv2_WDL
{
	CUP_HEADER;
	displayName  = "PASGT Helmet (Front Cover, M81 Woodland)";
	hiddenSelections[] = {"camo", "NVG_mount", "Goggle_Glass", "Goggle_ESS", "Cover_Front", "Cover_Back"};
	hiddenSelectionsTextures[] = {
		"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\data\CUP_H_PASGT_CO.paa"
	};
	class ItemInfo: ItemInfo
	{
		hiddenSelections[] = {"camo", "NVG_mount", "Cover_Back"};
		hiddenSelectionsTextures[] = {
			"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\data\CUP_H_PASGT_CO.paa"
		};
	};
};

class CUP_H_PASGTv2_WDL_GG: ItemCore
{
	CUP_HEADER_PUBLIC;
	displayName  = "PASGT Helmet (Goggles, M81 Woodland)";
	descriptionShort = "$STR_A3_SP_AL_II";
	picture = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USMC\data\ui\icon_H_USMC_HelmetWDL_ca.paa";
	uniformModel = "\cup\creatures\people\military\cup_creatures_people_military_usarmy\CUP_H_PASGTv2.p3d";
	hiddenSelections[] = {"camo", "NVG_mount", "Goggle_Glass", "Goggle_ESS", "Cover_Front", "Cover_Back"};
	hiddenSelectionsTextures[] = {
		"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\data\CUP_H_PASGT_CO.paa"
	};
	class ItemInfo: HeadgearItem
	{
		mass = 40;
		uniformModel = "\cup\creatures\people\military\cup_creatures_people_military_usarmy\CUP_H_PASGTv2.p3d";
		allowedSlots[] = {UNIFORM_SLOT, BACKPACK_SLOT, VEST_SLOT, HEADGEAR_SLOT};
		modelSides[] = {6};
		armor = 3;
		passThrough = 0.5;

		hiddenSelections[] = {"camo", "NVG_mount", "Cover_Front", "Cover_Back"};
		hiddenSelectionsTextures[] = {
			"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\data\CUP_H_PASGT_CO.paa"
		};
		#include "\CUP\Creatures\hitpoints_headmid.h"
	};
};
// PASGTv2 camo variants
class CUP_H_PASGTv2_ERDL_highland: CUP_H_PASGTv2_WDL
{
	CUP_HEADER;
	displayName  = "PASGT Helmet (ERDL Highland)";
	hiddenSelectionsTextures[] = {
		"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\data\CUP_H_PASGT_ERDL_highland_CO.paa"
	};
	class ItemInfo: ItemInfo
	{
		hiddenSelectionsTextures[] = {
			"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\data\CUP_H_PASGT_ERDL_highland_CO.paa"
		};
	};
};
class CUP_H_PASGTv2_NVG_ERDL_highland: CUP_H_PASGTv2_WDL
{
	CUP_HEADER;
	displayName  = "PASGT Helmet (NVG, ERDL Highland)";
	hiddenSelectionsTextures[] = {
		"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\data\CUP_H_PASGT_ERDL_highland_CO.paa",
		"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USMC\data\new_usmc_gear3_tan_co.paa"
	};
	class ItemInfo: ItemInfo
	{
		hiddenSelectionsTextures[] = {
			"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\data\CUP_H_PASGT_ERDL_highland_CO.paa",
			"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USMC\data\new_usmc_gear3_tan_co.paa"
		};
	};
};
class CUP_H_PASGTv2_ERDL_lowland: CUP_H_PASGTv2_WDL
{
	CUP_HEADER;
	displayName  = "PASGT Helmet (ERDL Lowland)";
	hiddenSelectionsTextures[] = {
		"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\data\CUP_H_PASGT_ERDL_lowland_CO.paa"
	};
	class ItemInfo: ItemInfo
	{
		hiddenSelectionsTextures[] = {
			"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\data\CUP_H_PASGT_ERDL_lowland_CO.paa"
		};
	};
};
class CUP_H_PASGTv2_NVG_ERDL_lowland: CUP_H_PASGTv2_WDL
{
	CUP_HEADER;
	displayName  = "PASGT Helmet (NVG, ERDL Lowland)";
	hiddenSelectionsTextures[] = {
		"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\data\CUP_H_PASGT_ERDL_lowland_CO.paa",
		"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USMC\data\new_usmc_gear3_tan_co.paa"
	};
	class ItemInfo: ItemInfo
	{
		hiddenSelectionsTextures[] = {
			"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\data\CUP_H_PASGT_ERDL_lowland_CO.paa",
			"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USMC\data\new_usmc_gear3_tan_co.paa"
		};
	};
};
class CUP_H_PASGTv2_tigerstripe: CUP_H_PASGTv2_WDL
{
	CUP_HEADER;
	displayName  = "PASGT Helmet (Tigerstripe)";
	hiddenSelectionsTextures[] = {
		"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\data\CUP_H_PASGT_tigerstripe_CO.paa"
	};
	class ItemInfo: ItemInfo
	{
		hiddenSelections[] = {"camo", "NVG_mount", "Goggle_Glass", "Goggle_ESS", "Cover_Front", "Cover_Back"};
		hiddenSelectionsTextures[] = {
			"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\data\CUP_H_PASGT_tigerstripe_CO.paa"
		};
	};
};
class CUP_H_PASGTv2_NVG_tigerstripe: CUP_H_PASGTv2_WDL
{
	CUP_HEADER;
	displayName  = "PASGT Helmet (NVG, Tigerstripe)";
	hiddenSelectionsTextures[] = {
		"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\data\CUP_H_PASGT_tigerstripe_CO.paa",
		"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USMC\data\new_usmc_gear3_tan_co.paa"
	};
	class ItemInfo: ItemInfo
	{
		hiddenSelectionsTextures[] = {
			"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\data\CUP_H_PASGT_tigerstripe_CO.paa",
			"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USMC\data\new_usmc_gear3_tan_co.paa"
		};
	};
};
class CUP_H_PASGTv2_desert: CUP_H_PASGTv2_WDL
{
	CUP_HEADER;
	displayName  = "PASGT Helmet (Desert)";
	hiddenSelectionsTextures[] = {
		"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\data\CUP_H_PASGT_desert_CO.paa"
	};
	class ItemInfo: ItemInfo
	{
		hiddenSelectionsTextures[] = {
			"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\data\CUP_H_PASGT_desert_CO.paa"
		};
	};
};
class CUP_H_PASGTv2_NVG_desert: CUP_H_PASGTv2_WDL
{
	CUP_HEADER;
	displayName  = "PASGT Helmet (NVG, Desert)";
	hiddenSelectionsTextures[] = {
		"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\data\CUP_H_PASGT_desert_CO.paa",
		"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USMC\data\new_usmc_gear3_tan_co.paa"
	};
	class ItemInfo: ItemInfo
	{
		hiddenSelectionsTextures[] = {
			"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\data\CUP_H_PASGT_desert_CO.paa",
			"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USMC\data\new_usmc_gear3_tan_co.paa"
		};
	};
};
class CUP_H_PASGTv2_winter: CUP_H_PASGTv2_WDL
{
	CUP_HEADER;
	displayName  = "PASGT Helmet (Winter)";
	hiddenSelectionsTextures[] = {
		"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\data\CUP_H_PASGT_winter_CO.paa"
	};
	class ItemInfo: ItemInfo
	{
		hiddenSelectionsTextures[] = {
			"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\data\CUP_H_PASGT_winter_CO.paa"
		};
	};
};
class CUP_H_PASGTv2_NVG_winter: CUP_H_PASGTv2_WDL
{
	CUP_HEADER;
	displayName  = "PASGT Helmet (NVG, Winter)";
	hiddenSelectionsTextures[] = {
		"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\data\CUP_H_PASGT_winter_CO.paa",
		"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USMC\data\new_usmc_gear3_tan_co.paa"
	};
	class ItemInfo: ItemInfo
	{
		hiddenSelectionsTextures[] = {
			"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\data\CUP_H_PASGT_winter_CO.paa",
			"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USMC\data\new_usmc_gear3_tan_co.paa"
		};
	};
};
class CUP_H_PASGTv2_DCU: CUP_H_PASGTv2_WDL
{
	CUP_HEADER;
	displayName  = "PASGT Helmet (DCU)";
	hiddenSelectionsTextures[] = {
		"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\data\CUP_H_PASGT_DCU_CO.paa"
	};
	class ItemInfo: ItemInfo
	{
		hiddenSelectionsTextures[] = {
			"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\data\CUP_H_PASGT_DCU_CO.paa"
		};
	};
};
class CUP_H_PASGTv2_NVG_DCU: CUP_H_PASGTv2_WDL
{
	CUP_HEADER;
	displayName  = "PASGT Helmet (NVG, DCU)";
	hiddenSelectionsTextures[] = {
		"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\data\CUP_H_PASGT_DCU_CO.paa",
		"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USMC\data\new_usmc_gear3_tan_co.paa"
	};
	class ItemInfo: ItemInfo
	{
		hiddenSelectionsTextures[] = {
			"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\data\CUP_H_PASGT_DCU_CO.paa",
			"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USMC\data\new_usmc_gear3_tan_co.paa"
		};
	};
};
class CUP_H_PASGTv2_OD: CUP_H_PASGTv2_WDL
{
	CUP_HEADER;
	displayName  = "PASGT Helmet (Olive)";
	hiddenSelectionsTextures[] = {
		"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\data\CUP_H_PASGT_OD_CO.paa"
	};
	class ItemInfo: ItemInfo
	{
		hiddenSelectionsTextures[] = {
			"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\data\CUP_H_PASGT_OD_CO.paa"
		};
	};
};
class CUP_H_PASGTv2_NVG_OD: CUP_H_PASGTv2_WDL
{
	CUP_HEADER;
	displayName  = "PASGT Helmet (NVG, Olive)";
	hiddenSelectionsTextures[] = {
		"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\data\CUP_H_PASGT_OD_CO.paa",
		"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USMC\data\new_usmc_gear3_tan_co.paa"
	};
	class ItemInfo: ItemInfo
	{
		hiddenSelectionsTextures[] = {
			"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\data\CUP_H_PASGT_OD_CO.paa",
			"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USMC\data\new_usmc_gear3_tan_co.paa"
		};
	};
};
class CUP_H_PASGTv2_TPattern: CUP_H_PASGTv2_WDL
{
	CUP_HEADER;
	displayName  = "PASGT Helmet (T-pattern)";
	hiddenSelectionsTextures[] = {
		"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\data\CUP_H_PASGT_TPattern_CO.paa"
	};
	class ItemInfo: ItemInfo
	{
		hiddenSelectionsTextures[] = {
			"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\data\CUP_H_PASGT_TPattern_CO.paa"
		};
	};
};
class CUP_H_PASGTv2_NVG_TPattern: CUP_H_PASGTv2_WDL
{
	CUP_HEADER;
	displayName  = "PASGT Helmet (NVG, T-pattern)";
	hiddenSelectionsTextures[] = {
		"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\data\CUP_H_PASGT_TPattern_CO.paa",
		"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USMC\data\new_usmc_gear3_tan_co.paa"
	};
	class ItemInfo: ItemInfo
	{
		hiddenSelectionsTextures[] = {
			"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\data\CUP_H_PASGT_TPattern_CO.paa",
			"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USMC\data\new_usmc_gear3_tan_co.paa"
		};
	};
};
class CUP_H_PASGTv2_Urban: CUP_H_PASGTv2_WDL
{
	CUP_HEADER;
	displayName  = "PASGT Helmet (Urban)";
	hiddenSelectionsTextures[] = {
		"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\data\CUP_H_PASGT_Urban_CO.paa"
	};
	class ItemInfo: ItemInfo
	{
		hiddenSelectionsTextures[] = {
			"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\data\CUP_H_PASGT_Urban_CO.paa"
		};
	};
};
class CUP_H_PASGTv2_NVG_Urban: CUP_H_PASGTv2_WDL
{
	CUP_HEADER;
	displayName  = "PASGT Helmet (NVG, Urban)";
	hiddenSelectionsTextures[] = {
		"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\data\CUP_H_PASGT_Urban_CO.paa",
		"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USMC\data\new_usmc_gear3_tan_co.paa"
	};
	class ItemInfo: ItemInfo
	{
		hiddenSelectionsTextures[] = {
			"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\data\CUP_H_PASGT_Urban_CO.paa",
			"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USMC\data\new_usmc_gear3_tan_co.paa"
		};
	};
};
// PASGTv2 end

// PASGT old
class CUP_H_US_H_PASGT_WDL: ItemCore
{
	CUP_HEADER_PROTECTED;
	displayName  = "PASGT Helmet (M81 Woodland)";
	descriptionShort = "$STR_A3_SP_AL_II";
	picture = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USMC\data\ui\icon_H_USMC_HelmetWDL_ca.paa";
	uniformModel = "\cup\creatures\people\military\cup_creatures_people_military_usarmy\CUP_US_PASGT_helmet.p3d";
	hiddenSelections[] = {"camo"};
	hiddenSelectionsTextures[] = {"\cup\creatures\people\military\cup_creatures_people_military_usarmy\data\US_helmet_PASGT_co.paa"};
	class ItemInfo: HeadgearItem
	{
		mass = 40;
		uniformModel = "\cup\creatures\people\military\cup_creatures_people_military_usarmy\CUP_US_PASGT_helmet.p3d";
		allowedSlots[] = {UNIFORM_SLOT, BACKPACK_SLOT, VEST_SLOT, HEADGEAR_SLOT};
		modelSides[] = {6};
		armor = 3;
		passThrough = 0.5;
		hiddenSelections[] = {"camo"};
		hiddenSelectionsTextures[] = {"\cup\creatures\people\military\cup_creatures_people_military_usarmy\data\US_helmet_PASGT_co.paa"};
		#include "\CUP\Creatures\hitpoints_headmid.h"
	};
};
class CUP_H_US_H_PASGT_desert: ItemCore
{
	CUP_HEADER_PROTECTED;
	displayName  = "PASGT Helmet (Desert)";
	descriptionShort = "$STR_A3_SP_AL_II";
	picture = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USMC\data\ui\icon_H_USMC_HelmetWDL_ca.paa";
	uniformModel = "\cup\creatures\people\military\cup_creatures_people_military_usarmy\CUP_US_PASGT_helmet.p3d";
	hiddenSelections[] = {"camo"};
	hiddenSelectionsTextures[] = {"\cup\creatures\people\military\cup_creatures_people_military_usarmy\data\US_helmet_PASGT_desert_co.paa"};
	class ItemInfo: HeadgearItem
	{
		mass = 40;
		uniformModel = "\cup\creatures\people\military\cup_creatures_people_military_usarmy\CUP_US_PASGT_helmet.p3d";
		allowedSlots[] = {UNIFORM_SLOT, BACKPACK_SLOT, VEST_SLOT, HEADGEAR_SLOT};
		modelSides[] = {6};
		armor = 3;
		passThrough = 0.5;
		hiddenSelections[] = {"camo"};
		hiddenSelectionsTextures[] = {"\cup\creatures\people\military\cup_creatures_people_military_usarmy\data\US_helmet_PASGT_desert_co.paa"};
		#include "\CUP\Creatures\hitpoints_headmid.h"
	};
};
class CUP_H_US_H_PASGT_winter: ItemCore
{
	CUP_HEADER_PROTECTED;
	displayName  = "PASGT Helmet (Winter)";
	descriptionShort = "$STR_A3_SP_AL_II";
	picture = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USMC\data\ui\icon_H_USMC_HelmetWDL_ca.paa";
	uniformModel = "\cup\creatures\people\military\cup_creatures_people_military_usarmy\CUP_US_PASGT_helmet.p3d";
	hiddenSelections[] = {"camo"};
	hiddenSelectionsTextures[] = {"\cup\creatures\people\military\cup_creatures_people_military_usarmy\data\US_helmet_PASGT_winter_co.paa"};
	class ItemInfo: HeadgearItem
	{
		mass = 40;
		uniformModel = "\cup\creatures\people\military\cup_creatures_people_military_usarmy\CUP_US_PASGT_helmet.p3d";
		allowedSlots[] = {UNIFORM_SLOT, BACKPACK_SLOT, VEST_SLOT, HEADGEAR_SLOT};
		modelSides[] = {6};
		armor = 3;
		passThrough = 0.5;
		hiddenSelections[] = {"camo"};
		hiddenSelectionsTextures[] = {"\cup\creatures\people\military\cup_creatures_people_military_usarmy\data\US_helmet_PASGT_winter_co.paa"};
		#include "\CUP\Creatures\hitpoints_headmid.h"
	};
};
class CUP_H_US_patrol_cap_WDL: ItemCore
{
	CUP_HEADER_PUBLIC;
	displayName  = "Patrol Cap (M81 Woodland)";
	descriptionShort = "$STR_A3_SP_NOARMOR";
	picture = "\A3\characters_f\Data\UI\icon_H_Cap_blk_CA.paa";
	uniformModel = "\cup\creatures\people\military\cup_creatures_people_military_usarmy\CUP_US_patrol_cap.p3d";
	hiddenSelections[] = {"camo"};
	hiddenSelectionsTextures[] = {"\cup\creatures\people\military\cup_creatures_people_military_usarmy\data\patrol_cap_co.paa"};
	class ItemInfo: HeadgearItem
	{
		mass = 10;
		uniformModel = "\cup\creatures\people\military\cup_creatures_people_military_usarmy\CUP_US_patrol_cap.p3d";
		allowedSlots[] = {UNIFORM_SLOT, BACKPACK_SLOT, VEST_SLOT, HEADGEAR_SLOT};
		modelSides[] = {6};
		armor = 0;
		passThrough = 1;
		hiddenSelections[] = {"camo"};
		hiddenSelectionsTextures[] = {"\cup\creatures\people\military\cup_creatures_people_military_usarmy\data\patrol_cap_co.paa"};
		#include "\CUP\Creatures\hitpoints_headno.h"
	};
};
class CUP_H_US_patrol_cap_OD: CUP_H_US_patrol_cap_WDL
{
	CUP_HEADER;
	displayName  = "Patrol Cap (Olive)";
	hiddenSelectionsTextures[] = {"\cup\creatures\people\military\cup_creatures_people_military_usarmy\data\patrol_cap_OD_co.paa"};
	class ItemInfo: ItemInfo
	{
		hiddenSelectionsTextures[] = {"\cup\creatures\people\military\cup_creatures_people_military_usarmy\data\patrol_cap_OD_co.paa"};
	};
};
class CUP_H_US_patrol_cap_winter: CUP_H_US_patrol_cap_WDL
{
	CUP_HEADER;
	displayName  = "Patrol Cap (Winter)";
	hiddenSelectionsTextures[] = {"\cup\creatures\people\military\cup_creatures_people_military_usarmy\data\patrol_cap_winter_co.paa"};
	class ItemInfo: ItemInfo
	{
		hiddenSelectionsTextures[] = {"\cup\creatures\people\military\cup_creatures_people_military_usarmy\data\patrol_cap_winter_co.paa"};
	};
};
class CUP_H_US_patrol_cap_desert: CUP_H_US_patrol_cap_WDL
{
	CUP_HEADER;
	displayName  = "Patrol Cap (Desert)";
	hiddenSelectionsTextures[] = {"\cup\creatures\people\military\cup_creatures_people_military_usarmy\data\patrol_cap_desert_co.paa"};
	class ItemInfo: ItemInfo
	{
		hiddenSelectionsTextures[] = {"\cup\creatures\people\military\cup_creatures_people_military_usarmy\data\patrol_cap_desert_co.paa"};
	};
};
class CUP_H_US_patrol_cap_ERDL: CUP_H_US_patrol_cap_WDL
{
	CUP_HEADER;
	displayName  = "Patrol Cap (ERDL Lowland)";
	hiddenSelectionsTextures[] = {"\cup\creatures\people\military\cup_creatures_people_military_usarmy\data\patrol_cap_ERDL_co.paa"};
	class ItemInfo: ItemInfo
	{
		hiddenSelectionsTextures[] = {"\cup\creatures\people\military\cup_creatures_people_military_usarmy\data\patrol_cap_ERDL_co.paa"};
	};
};
class CUP_H_US_patrol_cap_ERDL_highland: CUP_H_US_patrol_cap_WDL
{
	CUP_HEADER;
	displayName  = "Patrol Cap (ERDL Highland)";
	hiddenSelectionsTextures[] = {"\cup\creatures\people\military\cup_creatures_people_military_usarmy\data\patrol_cap_ERDL_highland_co.paa"};
	class ItemInfo: ItemInfo
	{
		hiddenSelectionsTextures[] = {"\cup\creatures\people\military\cup_creatures_people_military_usarmy\data\patrol_cap_ERDL_highland_co.paa"};
	};
};
class CUP_H_US_patrol_cap_tigerstripe: CUP_H_US_patrol_cap_WDL
{
	CUP_HEADER;
	displayName  = "Patrol Cap (Tiger Stripe)";
	hiddenSelectionsTextures[] = {"\cup\creatures\people\military\cup_creatures_people_military_usarmy\data\patrol_cap_tigerstripe_co.paa"};
	class ItemInfo: ItemInfo
	{
		hiddenSelectionsTextures[] = {"\cup\creatures\people\military\cup_creatures_people_military_usarmy\data\patrol_cap_tigerstripe_co.paa"};
	};
};
class CUP_H_US_patrol_cap_Tpattern: CUP_H_US_patrol_cap_WDL
{
	CUP_HEADER;
	displayName  = "Patrol Cap (T-pattern)";
	hiddenSelectionsTextures[] = {"\cup\creatures\people\military\cup_creatures_people_military_usarmy\data\patrol_cap_Tpattern_co.paa"};
	class ItemInfo: ItemInfo
	{
		hiddenSelectionsTextures[] = {"\cup\creatures\people\military\cup_creatures_people_military_usarmy\data\patrol_cap_Tpattern_co.paa"};
	};
};
class CUP_H_US_patrol_cap_urban: CUP_H_US_patrol_cap_WDL
{
	CUP_HEADER;
	displayName  = "Patrol Cap (Urban)";
	hiddenSelectionsTextures[] = {"\cup\creatures\people\military\cup_creatures_people_military_usarmy\data\patrol_cap_urban_co.paa"};
	class ItemInfo: ItemInfo
	{
		hiddenSelectionsTextures[] = {"\cup\creatures\people\military\cup_creatures_people_military_usarmy\data\patrol_cap_urban_co.paa"};
	};
};
class CUP_H_US_patrol_cap_DCU: CUP_H_US_patrol_cap_WDL
{
	CUP_HEADER;
	displayName  = "Patrol Cap (DCU)";
	hiddenSelectionsTextures[] = {"\cup\creatures\people\military\cup_creatures_people_military_usarmy\data\patrol_cap_DCU_co.paa"};
	class ItemInfo: ItemInfo
	{
		hiddenSelectionsTextures[] = {"\cup\creatures\people\military\cup_creatures_people_military_usarmy\data\patrol_cap_DCU_co.paa"};
	};
};

class CUP_H_US_patrol_cap_UCP: CUP_H_US_patrol_cap_WDL
{
	CUP_HEADER;
	displayName  = "Patrol Cap (UCP)";
	hiddenSelectionsTextures[] = {"\cup\creatures\people\military\cup_creatures_people_military_usarmy\data\patrol_cap_ucp_co.paa"};
	class ItemInfo: ItemInfo
	{
		hiddenSelectionsTextures[] = {"\cup\creatures\people\military\cup_creatures_people_military_usarmy\data\patrol_cap_ucp_co.paa"};
	};
};

class CUP_H_US_patrol_cap_OCP: CUP_H_US_patrol_cap_WDL
{
	CUP_HEADER;
	displayName  = "Patrol Cap (OCP)";
	hiddenSelectionsTextures[] = {"\cup\creatures\people\military\cup_creatures_people_military_usarmy\data\patrol_cap_ocp_co.paa"};
	class ItemInfo: ItemInfo
	{
		hiddenSelectionsTextures[] = {"\cup\creatures\people\military\cup_creatures_people_military_usarmy\data\patrol_cap_ocp_co.paa"};
	};
};

class CUP_H_US_patrol_cap_OEFCP: CUP_H_US_patrol_cap_WDL
{
	CUP_HEADER;
	displayName  = "Patrol Cap (OEF-CP)";
	hiddenSelectionsTextures[] = {"\cup\creatures\people\military\cup_creatures_people_military_usarmy\data\patrol_cap_oefcp_co.paa"};
	class ItemInfo: ItemInfo
	{
		hiddenSelectionsTextures[] = {"\cup\creatures\people\military\cup_creatures_people_military_usarmy\data\patrol_cap_oefcp_co.paa"};
	};
};
class CUP_H_US_BOONIE_Alpenflage: ItemCore
{
	CUP_HEADER_PUBLIC;
	displayName  = "Boonie (Alpenflage)";
	descriptionShort = "$STR_A3_SP_NOARMOR";
	picture = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USMC\data\ui\icon_h_Boonie_1_ca.paa";
	model   = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USMC\CUP_USMC_Boonie_1.p3d";
	hiddenSelections[] = {"camo"};
	hiddenSelectionsTextures[] = {"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\data\new_alpenflage_boonie_co.paa"};
	class ItemInfo: HeadgearItem
	{
		mass = 5;
		uniformModel = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USMC\CUP_USMC_Boonie_1.p3d";
		allowedSlots[] = {UNIFORM_SLOT, BACKPACK_SLOT, VEST_SLOT, HEADGEAR_SLOT};
		modelSides[] = {6};
		armor = 0;
		passThrough = 1;
		hiddenSelections[] = {"camo"};
		hiddenSelectionsTextures[] = {"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\data\new_alpenflage_boonie_co.paa"};
		#include "\CUP\Creatures\hitpoints_headno.h"
	};
};

class CUP_H_US_patrol_cap_alpenflage: CUP_H_US_patrol_cap_WDL
{
	CUP_HEADER;
	displayName  = "Patrol Cap (Alpenflage)";
	hiddenSelectionsTextures[] = {"\cup\creatures\people\military\cup_creatures_people_military_usarmy\data\patrol_cap_alpenflage_co.paa"};
	class ItemInfo: ItemInfo
	{
		hiddenSelectionsTextures[] = {"\cup\creatures\people\military\cup_creatures_people_military_usarmy\data\patrol_cap_alpenflage_co.paa"};
	};
};

//SPH-4 pilot helmet


class CUP_H_SPH4 : ItemCore
{
	CUP_HEADER_PUBLIC;
	displayName  = "SPH-4 (OD)";
	descriptionShort = "$STR_A3_SP_AL_I";
	picture = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_BAF\CUP_headgear\pilot\ui\icon_h_baf_pilot_ca.paa";
	model   = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\CUP_H_SPH4.p3d";
	hiddenSelections[] = {"Camo"};
	hiddenSelectionsTextures[] = {"CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\data\SPH4\SPH4_CO.paa"};
	class ItemInfo: HeadgearItem
	{
		mass = 40;
		uniformModel = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\CUP_H_SPH4.p3d";
		allowedSlots[] = {UNIFORM_SLOT, BACKPACK_SLOT, VEST_SLOT, HEADGEAR_SLOT};
		modelSides[] = {6};
		armor = 3;
		passThrough = 0.5;
	    hiddenSelections[] = {"Camo"};
		hiddenSelectionsTextures[] = {"CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\data\SPH4\SPH4_CO.paa"};
		#include "\CUP\Creatures\hitpoints_headlight.h"
	};
	ace_hearing_protection = 0.85;
	ace_hearing_lowerVolume = 0.6;
};

class CUP_H_SPH4_visor : CUP_H_SPH4
{
	CUP_HEADER_PUBLIC;
	displayName  = "SPH-4 (OD/Visor)";
	model = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\CUP_H_SPH4_visor.p3d";
	class ItemInfo: ItemInfo {
		uniformModel = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\CUP_H_SPH4_visor.p3d";
	};
};

class CUP_H_SPH4_green : CUP_H_SPH4
{
	CUP_HEADER_PUBLIC;
	displayName  = "SPH-4 (Green)";
	hiddenSelectionsTextures[] = {"CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\data\SPH4\SPH4_green_CO.paa"};
	class ItemInfo: ItemInfo {
		hiddenSelectionsTextures[] = {"CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\data\SPH4\SPH4_green_CO.paa"};
	};
};

class CUP_H_SPH4_green_visor : CUP_H_SPH4_green
{
	CUP_HEADER_PUBLIC;
	displayName  = "SPH-4 (Green/Visor)";
	model = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\CUP_H_SPH4_visor.p3d";
	class ItemInfo: ItemInfo {
		uniformModel = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\CUP_H_SPH4_visor.p3d";
	};
};

class CUP_H_SPH4_khaki: CUP_H_SPH4
{
	CUP_HEADER_PUBLIC;
	displayName  = "SPH-4 (Khaki)";
	hiddenSelectionsTextures[] = {"CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\data\SPH4\SPH4_khaki_CO.paa"};
	class ItemInfo: ItemInfo {
		hiddenSelectionsTextures[] = {"CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\data\SPH4\SPH4_khaki_CO.paa"};
	};
};

class CUP_H_SPH4_khaki_visor : CUP_H_SPH4_khaki
{
	CUP_HEADER_PUBLIC;
	displayName  = "SPH-4 (Khaki/Visor)";
	model = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\CUP_H_SPH4_visor.p3d";
	class ItemInfo: ItemInfo {
		uniformModel = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\CUP_H_SPH4_visor.p3d";
	};
};

class CUP_H_SPH4_grey: CUP_H_SPH4
{
	CUP_HEADER_PUBLIC;
	displayName  = "SPH-4 (Grey)";
	hiddenSelectionsTextures[] = {"CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\data\SPH4\SPH4_grey_CO.paa"};
	class ItemInfo: ItemInfo {
		hiddenSelectionsTextures[] = {"CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\data\SPH4\SPH4_grey_CO.paa"};
	};
};

class CUP_H_SPH4_grey_visor : CUP_H_SPH4_grey
{
	CUP_HEADER_PUBLIC;
	displayName  = "SPH-4 (Grey/Visor)";
	model = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\CUP_H_SPH4_visor.p3d";
	class ItemInfo: ItemInfo {
		uniformModel = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\CUP_H_SPH4_visor.p3d";
	};
};

// Combat Crew Vehicle Helmet


class CUP_H_CVC : ItemCore
{
	CUP_HEADER_PUBLIC;
	displayName = "CVC-H";
	picture = "\A3\characters_F_Beta\Data\UI\icon_H_I_Helmet_crew_ca.paa";
	model = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\CUP_H_CVCH.p3d";
	hiddenSelections[] = {"Camo"};
	hiddenSelectionsTextures[] = {"\A3\Characters_F_Beta\Indep\Data\headgear_ia_helmet_crew_co.paa"};
	class ItemInfo: HeadgearItem
	{
		mass = 40;
		uniformModel = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\CUP_H_CVCH.p3d";
		allowedSlots[] = {UNIFORM_SLOT, BACKPACK_SLOT, VEST_SLOT, HEADGEAR_SLOT};
		modelSides[] = {6};
		armor = 3;
		passThrough = 0.5;
	    hiddenSelections[] = {"Camo"};
		hiddenSelectionsTextures[] = {"\A3\Characters_F_Beta\Indep\Data\headgear_ia_helmet_crew_co.paa"};
		#include "\CUP\Creatures\hitpoints_headlight.h"
	};
	ace_hearing_protection = 0.85;
	ace_hearing_lowerVolume = 0.6;
};

class CUP_H_CVCH_des: CUP_H_CVC
{
	CUP_HEADER_PUBLIC;
	displayName = "CVC-H (Desert)";
	hiddenSelectionsTextures[] = {"CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\data\CUP_H_CVCH_des_CO.paa"};
	class ItemInfo: ItemInfo {
		hiddenSelectionsTextures[] = {"CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\data\CUP_H_CVCH_des_CO.paa"};
	};
};