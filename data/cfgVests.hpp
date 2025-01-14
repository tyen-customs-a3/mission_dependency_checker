class VestItem: InventoryItem_Base_F
{
	type = VEST_SLOT;			/// vests fit into vest slot
	hiddenSelections[] = {};	/// no changeable selections by default
	armor = 5*0;				/// what protection does the vest provide
	passThrough = 1;			/// coef of damage passed to total damage
	hitpointName = "HitBody";	/// name of hitpoint shielded by the vest
};

class CUP_Vest_Camo_Base: ItemCore
{
    CUP_HEADER_PRIVATE;
	allowedSlots[] = {BACKPACK_SLOT};
	hiddenSelections[] = {"camo1", "camo2"};
	descriptionShort = "$STR_A3_SP_NOARMOR";

	class ItemInfo: VestItem
	{
		hiddenSelections[] = {"camo", "camo1", "camo2"};
		armor = 0;
		passThrough = 1;
		mass = 0;
		containerClass = "Supply0";
		#include "\CUP\Creatures\hitpoints_vestno.h"
	};
};

//PILOT
class CUP_V_B_USArmy_PilotVest: CUP_Vest_Camo_Base
{
    CUP_HEADER_PUBLIC;
	displayName  = "Pilot Vest [US Army]";
	descriptionShort = "$STR_A3_SP_AL_II";
	picture = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USMC\data\ui\icon_v_usmc_pilot_vest_ca.paa";
	model   = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\CUP_USArmy_Pilot_Vest.p3d";
	hiddenSelections[] = {"Camo"};
	hiddenSelectionsTextures[] = {"cup\creatures\people\military\cup_creatures_people_military_usarmy\data\usarmy_pilot_co.paa"};
	class ItemInfo: ItemInfo
	{
		hiddenSelections[] = {"Camo"};
		containerClass = "Supply80";
		uniformModel   = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\CUP_USArmy_Pilot_Vest.p3d";
		armor = 20;
		passThrough = 0.5;
		mass = 40;
		#include "\CUP\Creatures\hitpoints_vestmid.h"
	};
};
//RANGER
class CUP_V_B_RangerVest: CUP_Vest_Camo_Base
{
    CUP_HEADER_PRIVATE;
	displayName  = "US Ranger Assault Vest";
	descriptionShort = "$STR_A3_SP_AL_III";
	picture = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USMC\data\ui\icon_v_modular_tactical_vest_patrol_ca.paa";
	model   = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\cup_v_usranger.p3d";

	class ItemInfo: ItemInfo
	{
		containerClass = "Supply100";
		uniformModel   = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\cup_v_usranger.p3d";
		armor = 20;
		passThrough = 0.5;
		mass = 80;
		#include "\CUP\Creatures\hitpoints_vestheavy.h"
	};
};

//ALICE
class CUP_V_B_ALICE: CUP_Vest_Camo_Base
{
    CUP_HEADER_PUBLIC;
	displayName  = "ALICE Webbing";
	descriptionShort = "$STR_A3_SP_NOARMOR";
	picture = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_Chedaki\data\ui\icon_v_pouch_carrier_ca.paa";
	model   = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\CUP_v_ALICE_webbing.p3d";
	hiddenSelections[] = {"camo1", "camo2"};
	hiddenSelectionsTextures[] = {
	"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\data\US_PASGT_vest_CO.paa", "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\data\US_PASGT_gear_CO.paa"};

	class ItemInfo: ItemInfo
	{
		containerClass = "Supply90";
		uniformModel   = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\CUP_v_ALICE_webbing.p3d";
		armor = 0;
		passThrough = 1;
		mass = 15;
		#include "\CUP\Creatures\hitpoints_vestno.h"
		hiddenSelections[] = {"camo1", "camo2"};
		hiddenSelectionsTextures[] = {
		"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\data\US_PASGT_vest_CO.paa", "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\data\US_PASGT_gear_CO.paa"};
	};
};

#include "CfgVests_PASGT.hpp"

// Interceptor
class CUP_V_B_Interceptor_Baseclass: CUP_Vest_Camo_Base
{
	CUP_HEADER_PRIVATE;
	// TODO: Add proper interceptor pictures
	picture = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USMC\data\ui\icon_v_modular_tactical_vest_patrol_ca.paa";
	descriptionShort = "$STR_A3_SP_AL_III";

	class ItemInfo: ItemInfo
	{
		armor = 20;
		passThrough = 0.5;
		mass = 70;
		#include "\CUP\Creatures\hitpoints_vestheavy.h"
	};
};

class CUP_V_B_Interceptor_Baseclass_Rifleman: CUP_V_B_Interceptor_Baseclass
{
	CUP_HEADER_PRIVATE;

	model   = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\interceptor_rifleman.p3d";

	hiddenSelectionsTextures[] = {"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\data\intcep\us_interceptor_m81_co.paa"};
	hiddenSelections[] = {"camo","camo1","camo2"};

	class ItemInfo: ItemInfo
	{
		containerClass = "Supply100";
		uniformModel   = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\interceptor_rifleman.p3d";
		hiddenSelections[] = {"camo","camo1","camo2"};
	};
};

class CUP_V_B_Interceptor_Baseclass_Grenadier: CUP_V_B_Interceptor_Baseclass
{
    CUP_HEADER_PRIVATE;

	model   = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\interceptor_gl.p3d";
	hiddenSelections[] = {"camo","camo1"};

	class ItemInfo: ItemInfo
	{
		containerClass = "Supply140";
		uniformModel   = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\interceptor_gl.p3d";
		hiddenSelections[] = {"camo","camo1"};
		#include "\CUP\Creatures\hitpoints_vestheavy.h"
	};
};

class CUP_V_B_Interceptor_Baseclass_Base: CUP_V_B_Interceptor_Baseclass
{
    CUP_HEADER_PRIVATE;

	picture = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USMC\data\ui\icon_v_modular_tactical_vest_patrol_ca.paa";
	model   = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\interceptor_base.p3d";

	hiddenSelections[] = {"camo"};

	class ItemInfo: ItemInfo
	{
		containerClass = "Supply100"; // Reduce?
		uniformModel   = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\interceptor_base.p3d";
		hiddenSelections[] = {"camo"};
	};
};
#include "CfgVests_Interceptor.hpp"

class CUP_V_B_CIRAS_Base: CUP_Vest_Camo_Base {
	CUP_HEADER_PRIVATE;
	descriptionShort = "$STR_A3_SP_AL_II";

	class ItemInfo: ItemInfo
	{
		mass = 100;

		class HitpointsProtectionInfo
		{
			class Chest
			{
				HitpointName = "HitChest";
				armor = 20;
				PassThrough = 0.200000;
			};
			class Diaphragm
			{
				HitpointName = "HitDiaphragm";
				armor = 20;
				PassThrough = 0.200000;
			};
			class Abdomen
			{
				hitpointName = "HitAbdomen";
				armor = 20;
				passThrough = 0.200000;
			};
			class Body
			{
				hitpointName = "HitBody";
				passThrough = 0.200000;
			};
		};
	};
};
#include "CfgVests_Ciras.hpp"

#include "cfgVests_deprecated.hpp"
