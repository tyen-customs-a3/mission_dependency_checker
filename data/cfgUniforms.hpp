class InventoryItem_Base_F;
class ItemCore;
class UniformItem: InventoryItem_Base_F
{
	type = UNIFORM_SLOT; /// to what slot does the uniform fit
};
class CUP_U_B_USA06_Officer_m81: ItemCore
{
    CUP_HEADER_PRIVATE;
	allowedSlots[] = {BACKPACK_SLOT};
	displayName = "US Army (M81)"; /// how would the stuff be displayed in inventory and on ground
	picture = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USMC\data\ui\icon_u_b_marpat_wdl_officer_ca.paa";
	model = "\A3\Characters_F\Common\Suitpacks\suitpack_universal_F.p3d"; /// how does the uniform look when put on ground
	hiddenSelections[] = {"Camo1", "Camo2"};
	hiddenSelectionsTextures[] = {
		"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\data\USA06_officer_m81.paa"
	};
	class ItemInfo: UniformItem
	{
		uniformModel = "-";
		uniformClass = CUP_B_USA06_Soldier_02;
		containerClass = Supply40;
		mass = 20;
	};
};
class CUP_U_B_USArmy_Base: ItemCore
{
    CUP_HEADER_PUBLIC;
	allowedSlots[] = {BACKPACK_SLOT};
	displayName = "US Army (Modern/ACU)"; /// how would the stuff be displayed in inventory and on ground
	picture = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USMC\data\ui\icon_u_b_marpat_wdl_officer_ca.paa";
	model = "\A3\Characters_F\Common\Suitpacks\suitpack_universal_F.p3d"; /// how does the uniform look when put on ground
	hiddenSelections[] = {"Camo", "Camo1"};
	hiddenSelectionsTextures[] = {
		"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\data\tex1_co.paa", "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\data\tex4_co.paa"
	};
	class ItemInfo: UniformItem
	{
		uniformModel = "-";
		uniformClass = CUP_B_USArmy_Soldier_01;
		containerClass = Supply40;
		mass = 20;
	};
};
class CUP_U_B_USArmy_TwoKnee: ItemCore
{
   	CUP_HEADER_PUBLIC;
	allowedSlots[] = {BACKPACK_SLOT};
	displayName = "US Army (ACU/Knees)"; /// how would the stuff be displayed in inventory and on ground
	picture = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USMC\data\ui\icon_u_b_marpat_wdl_officer_ca.paa";
	model = "\A3\Characters_F\Common\Suitpacks\suitpack_universal_F.p3d"; /// how does the uniform look when put on ground
	hiddenSelections[] = {"Camo", "Camo1"};
	hiddenSelectionsTextures[] = {
		"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\data\tex1_co.paa", "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\data\tex4_co.paa"
	};
	class ItemInfo: UniformItem
	{
		uniformModel = "-";
		uniformClass = CUP_B_USArmy_Soldier_02;
		containerClass = Supply40;
		mass = 20;
	};
};
class CUP_U_B_USArmy_UBACS: ItemCore
{
    CUP_HEADER_PUBLIC;
	allowedSlots[] = {BACKPACK_SLOT};
	displayName = "US Army (UBACS/ACU)"; /// how would the stuff be displayed in inventory and on ground
	picture = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USMC\data\ui\icon_u_b_marpat_wdl_officer_ca.paa";
	model = "\A3\Characters_F\Common\Suitpacks\suitpack_universal_F.p3d"; /// how does the uniform look when put on ground
	hiddenSelections[] = {"Camo", "Camo2"};
	hiddenSelectionsTextures[] = {
		"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\data\tex1_co.paa", "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\data\ubacs_acu.paa"
	};
	class ItemInfo: UniformItem
	{
		uniformModel = "-";
		uniformClass = CUP_B_USArmy_Soldier_03;
		containerClass = Supply40;
		mass = 20;
	};
};
class CUP_U_B_USArmy_Soft: ItemCore
{
    CUP_HEADER_PUBLIC;
	allowedSlots[] = {BACKPACK_SLOT};
	displayName = "US Army (Soft Shell)"; /// how would the stuff be displayed in inventory and on ground
	picture = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USMC\data\ui\icon_u_b_marpat_wdl_officer_ca.paa";
	model = "\A3\Characters_F\Common\Suitpacks\suitpack_universal_F.p3d"; /// how does the uniform look when put on ground
	hiddenSelections[] = {"Camo"};
	hiddenSelectionsTextures[] = {
		"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\data\usarmy_softshell_acu_co.paa"};
	class ItemInfo: UniformItem
	{
		uniformModel = "-";
		uniformClass = CUP_B_USArmy_Soldier_04;
		containerClass = Supply40;
		mass = 20;
	};
};
class CUP_U_B_USArmy_Ghillie : ItemCore
{
	CUP_HEADER_PUBLIC;
	scopeArsenal = 0;
	allowedSlots[] = { BACKPACK_SLOT };
	displayName = "US Army Ghillie (desert)"; /// how would the stuff be displayed in inventory and on ground
	picture = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_Taki\data\ui\icon_u_o_tk_ghillie_ca.paa";
	model = "\A3\Characters_F\Common\Suitpacks\suitpack_universal_F.p3d"; /// how does the uniform look when put on ground
	class ItemInfo : UniformItem
	{
		uniformModel = "-";
		uniformClass = CUP_B_USArmy_Soldier_05;
		containerClass = Supply40;
		mass = 20;
	};
};
class CUP_U_B_USArmy_PilotOverall : ItemCore
{
	CUP_HEADER_PUBLIC;
	allowedSlots[] = { BACKPACK_SLOT };
	displayName = "Nomex Flightsuit (Ranger Green)"; /// how would the stuff be displayed in inventory and on ground
	picture = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USMC\data\ui\icon_u_b_usmc_pilotoverall_ca.paa";
	model = "\A3\Characters_F\Common\Suitpacks\suitpack_universal_F.p3d"; /// how does the uniform look when put on ground
	hiddenSelections[] = {"Camo", "Camo2"};
	class ItemInfo: UniformItem
	{
		uniformModel = "-";
		uniformClass = CUP_B_USArmy_Soldier_06;
		containerClass = Supply40;
		mass = 20;
	};
};

#include "cfgUniforms_BDUv2.hpp"

class CUP_U_B_US_BDU : ItemCore
{
	CUP_HEADER_PROTECTED;
	allowedSlots[] = { BACKPACK_SLOT };
	displayName = "BDU"; /// how would the stuff be displayed in inventory and on ground
	picture = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\data\ui\gear_u_b_bdu_woodland_ca.paa";
	model = "\A3\Characters_F\Common\Suitpacks\suitpack_universal_F.p3d"; /// how does the uniform look when put on ground
	hiddenSelections[] = {"camo", "camo1", "camo2"};
	hiddenSelectionsTextures[] = {
		"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USarmy\data\US_BDU_CO.paa",
		"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USarmy\data\US_BDU_CO.paa",
		"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USarmy\data\US_BDU_CO.paa"
	};
	class ItemInfo: UniformItem
	{
		uniformModel = "-";
		uniformClass = CUP_B_USArmy_Soldier_BDU;
		containerClass = Supply40;
		mass = 20;
	};
};
class CUP_U_B_US_BDU_OD : ItemCore
{
	CUP_HEADER_PROTECTED;
	allowedSlots[] = { BACKPACK_SLOT };
	displayName = "BDU (Olive)"; /// how would the stuff be displayed in inventory and on ground
	picture = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\data\ui\gear_u_b_bdu_od_ca.paa";
	model = "\A3\Characters_F\Common\Suitpacks\suitpack_universal_F.p3d"; /// how does the uniform look when put on ground
	hiddenSelections[] = {"camo", "camo1", "camo2"};
	hiddenSelectionsTextures[] = {
		"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USarmy\data\US_BDU_OD_CO.paa",
		"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USarmy\data\US_BDU_OD_CO.paa",
		"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USarmy\data\US_BDU_OD_CO.paa"
	};
	class ItemInfo: UniformItem
	{
		uniformModel = "-";
		uniformClass = CUP_B_USArmy_Soldier_BDU_OD;
		containerClass = Supply40;
		mass = 20;
	};
};
class CUP_U_B_US_BDU_desert : ItemCore
{
	CUP_HEADER_PROTECTED;
	allowedSlots[] = { BACKPACK_SLOT };
	displayName = "BDU (Desert)"; /// how would the stuff be displayed in inventory and on ground
	picture = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\data\ui\gear_u_b_bdu_3desert_ca.paa";
	model = "\A3\Characters_F\Common\Suitpacks\suitpack_universal_F.p3d"; /// how does the uniform look when put on ground
	hiddenSelections[] = {"camo", "camo1", "camo2"};
	hiddenSelectionsTextures[] = {
		"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USarmy\data\US_BDU_desert_CO.paa",
		"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USarmy\data\US_BDU_desert_CO.paa",
		"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USarmy\data\US_BDU_desert_CO.paa"
	};
	class ItemInfo: UniformItem
	{
		uniformModel = "-";
		uniformClass = CUP_B_USArmy_Soldier_BDU_desert;
		containerClass = Supply40;
		mass = 20;
	};
};
class CUP_U_B_US_BDU_ERDL : ItemCore
{
	CUP_HEADER_PROTECTED;
	allowedSlots[] = { BACKPACK_SLOT };
	displayName = "BDU (ERDL Lowland)"; /// how would the stuff be displayed in inventory and on ground
	picture = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\data\ui\gear_u_b_bdu_erdl_ca.paa";
	model = "\A3\Characters_F\Common\Suitpacks\suitpack_universal_F.p3d"; /// how does the uniform look when put on ground
	hiddenSelections[] = {"camo", "camo1", "camo2"};
	hiddenSelectionsTextures[] = {
		"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USarmy\data\US_BDU_ERDL_CO.paa",
		"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USarmy\data\US_BDU_ERDL_CO.paa",
		"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USarmy\data\US_BDU_ERDL_CO.paa"
	};
	class ItemInfo: UniformItem
	{
		uniformModel = "-";
		uniformClass = CUP_B_USArmy_Soldier_BDU_ERDL;
		containerClass = Supply40;
		mass = 20;
	};
};
class CUP_U_B_US_BDU_ERDL_highland : ItemCore
{
	CUP_HEADER_PROTECTED;
	allowedSlots[] = { BACKPACK_SLOT };
	displayName = "BDU (ERDL Highland)"; /// how would the stuff be displayed in inventory and on ground
	picture = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\data\ui\gear_u_b_bdu_erdl_highlands_ca.paa";
	model = "\A3\Characters_F\Common\Suitpacks\suitpack_universal_F.p3d"; /// how does the uniform look when put on ground
	hiddenSelections[] = {"camo", "camo1", "camo2"};
	hiddenSelectionsTextures[] = {
		"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USarmy\data\US_BDU_ERDL_highland_CO.paa",
		"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USarmy\data\US_BDU_ERDL_highland_CO.paa",
		"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USarmy\data\US_BDU_ERDL_highland_CO.paa"
	};
	class ItemInfo: UniformItem
	{
		uniformModel = "-";
		uniformClass = CUP_B_USArmy_Soldier_BDU_ERDL_highland;
		containerClass = Supply40;
		mass = 20;
	};
};
class CUP_U_B_US_BDU_tigerstripe : ItemCore
{
	CUP_HEADER_PROTECTED;
	allowedSlots[] = { BACKPACK_SLOT };
	displayName = "BDU (Tiger Stripe)"; /// how would the stuff be displayed in inventory and on ground
	picture = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\data\ui\gear_u_b_bdu_tigerstripes_ca.paa";
	model = "\A3\Characters_F\Common\Suitpacks\suitpack_universal_F.p3d"; /// how does the uniform look when put on ground
	hiddenSelections[] = {"camo", "camo1", "camo2"};
	hiddenSelectionsTextures[] = {
		"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USarmy\data\US_BDU_tigerstripe_CO.paa",
		"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USarmy\data\US_BDU_tigerstripe_CO.paa",
		"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USarmy\data\US_BDU_tigerstripe_CO.paa"
	};
	class ItemInfo: UniformItem
	{
		uniformModel = "-";
		uniformClass = CUP_B_USArmy_Soldier_BDU_tigerstripe;
		containerClass = Supply40;
		mass = 20;
	};
};
class CUP_U_B_US_BDU_Tpattern : ItemCore
{
	CUP_HEADER_PROTECTED;
	allowedSlots[] = { BACKPACK_SLOT };
	displayName = "BDU (T-pattern)"; /// how would the stuff be displayed in inventory and on ground
	picture = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\data\ui\gear_u_b_bdu_tpattern_ca.paa";
	model = "\A3\Characters_F\Common\Suitpacks\suitpack_universal_F.p3d"; /// how does the uniform look when put on ground
	hiddenSelections[] = {"camo", "camo1", "camo2"};
	hiddenSelectionsTextures[] = {
		"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USarmy\data\US_BDU_Tpattern_CO.paa",
		"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USarmy\data\US_BDU_Tpattern_CO.paa",
		"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USarmy\data\US_BDU_Tpattern_CO.paa"
	};
	class ItemInfo: UniformItem
	{
		uniformModel = "-";
		uniformClass = CUP_B_USArmy_Soldier_BDU_Tpattern;
		containerClass = Supply40;
		mass = 20;
	};
};
class CUP_U_B_US_BDU_urban : ItemCore
{
	CUP_HEADER_PROTECTED;
	allowedSlots[] = { BACKPACK_SLOT };
	displayName = "BDU (Urban)"; /// how would the stuff be displayed in inventory and on ground
	picture = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\data\ui\gear_u_b_bdu_urban_ca.paa";
	model = "\A3\Characters_F\Common\Suitpacks\suitpack_universal_F.p3d"; /// how does the uniform look when put on ground
	hiddenSelections[] = {"camo", "camo1", "camo2"};
	hiddenSelectionsTextures[] = {
		"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USarmy\data\US_BDU_urban_CO.paa",
		"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USarmy\data\US_BDU_urban_CO.paa",
		"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USarmy\data\US_BDU_urban_CO.paa"
	};
	class ItemInfo: UniformItem
	{
		uniformModel = "-";
		uniformClass = CUP_B_USArmy_Soldier_BDU_urban;
		containerClass = Supply40;
		mass = 20;
	};
};
class CUP_U_B_US_BDU_winter : ItemCore
{
	CUP_HEADER_PROTECTED;
	allowedSlots[] = { BACKPACK_SLOT };
	displayName = "BDU (Winter)"; /// how would the stuff be displayed in inventory and on ground
	picture = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\data\ui\gear_u_b_bdu_winter_ca.paa";
	model = "\A3\Characters_F\Common\Suitpacks\suitpack_universal_F.p3d"; /// how does the uniform look when put on ground
	hiddenSelections[] = {"camo", "camo1", "camo2"};
	hiddenSelectionsTextures[] = {
		"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USarmy\data\US_BDU_winter_CO.paa",
		"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USarmy\data\US_BDU_winter_CO.paa",
		"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USarmy\data\US_BDU_winter_CO.paa"
	};
	class ItemInfo: UniformItem
	{
		uniformModel = "-";
		uniformClass = CUP_B_USArmy_Soldier_BDU_winter;
		containerClass = Supply40;
		mass = 20;
	};
};
class CUP_U_B_US_BDU_winter_WoodlandBottom : ItemCore
{
	CUP_HEADER_PROTECTED;
	allowedSlots[] = { BACKPACK_SLOT };
	displayName = "BDU (Winter/Woodland)"; /// how would the stuff be displayed in inventory and on ground
	picture = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\data\ui\gear_u_b_bdu_winter_woodland_ca.paa";
	model = "\A3\Characters_F\Common\Suitpacks\suitpack_universal_F.p3d"; /// how does the uniform look when put on ground
	hiddenSelections[] = {"camo", "camo1", "camo2"};
	hiddenSelectionsTextures[] = {
		"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USarmy\data\US_BDU_CO.paa",
		"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USarmy\data\US_BDU_winter_CO.paa",
		"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USarmy\data\US_BDU_winter_CO.paa"
	};
	class ItemInfo: UniformItem
	{
		uniformModel = "-";
		uniformClass = CUP_B_USArmy_Soldier_BDU_winter_woodlandBottom;
		containerClass = Supply40;
		mass = 20;
	};
};
class CUP_U_B_US_BDU_winter_WoodlandTop : ItemCore
{
	CUP_HEADER_PROTECTED;
	allowedSlots[] = { BACKPACK_SLOT };
	displayName = "BDU (Woodland/Winter)"; /// how would the stuff be displayed in inventory and on ground
	picture = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\data\ui\gear_u_b_bdu_woodland_winter_ca.paa";
	model = "\A3\Characters_F\Common\Suitpacks\suitpack_universal_F.p3d"; /// how does the uniform look when put on ground
	hiddenSelections[] = {"camo", "camo1", "camo2"};
	hiddenSelectionsTextures[] = {
		"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USarmy\data\US_BDU_winter_CO.paa",
		"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USarmy\data\US_BDU_CO.paa",
		"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USarmy\data\US_BDU_winter_CO.paa"
	};
	class ItemInfo: UniformItem
	{
		uniformModel = "-";
		uniformClass = CUP_B_USArmy_Soldier_BDU_winter_WoodlandTop;
		containerClass = Supply40;
		mass = 20;
	};
};
class CUP_U_B_GER_BDU_Flecktarn: CUP_U_B_US_BDU
{
	CUP_HEADER_PROTECTED;
	displayName = "BDU (Flecktarn)";
	picture = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\data\ui\gear_u_b_bdu_flecktarn_ca.paa";
	hiddenSelections[] = {"camo", "camo1", "camo2"};
	hiddenSelectionsTextures[] = {
		"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USarmy\data\BDU_Flecktarn_co.paa",
		"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USarmy\data\BDU_Flecktarn_co.paa",
		"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USarmy\data\BDU_Flecktarn_co.paa"
	};
	class ItemInfo: UniformItem
	{
		uniformModel = "-";
		uniformClass = CUP_B_GER_Soldier_BDU_flecktarn;
		containerClass = Supply40;
		mass = 20;
	};
};
class CUP_U_B_GER_BDU_Flecktarn_ODBottom: CUP_U_B_US_BDU
{
	CUP_HEADER_PROTECTED;
	displayName = "BDU (Flecktarn/OD)";
	picture = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\data\ui\gear_u_b_bdu_flecktarn_od_ca.paa";
	hiddenSelections[] = {"camo", "camo1", "camo2"};
	hiddenSelectionsTextures[] = {
		"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USarmy\data\US_BDU_OD_CO.paa",
		"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USarmy\data\BDU_Flecktarn_co.paa",
		"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USarmy\data\BDU_Flecktarn_co.paa"
	};
	class ItemInfo: UniformItem
	{
		uniformModel = "-";
		uniformClass = CUP_B_GER_Soldier_BDU_flecktarn_ODBottom;
		containerClass = Supply40;
		mass = 20;
	};
};
class CUP_U_B_GER_BDU_Tropentarn: CUP_U_B_US_BDU
{
	CUP_HEADER_PROTECTED;
	displayName = "BDU (Tropentarn)";
	picture = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\data\ui\gear_u_b_bdu_tropentarn_ca.paa";
	hiddenSelections[] = {"camo", "camo1", "camo2"};
	hiddenSelectionsTextures[] = {
		"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USarmy\data\BDU_Tropentarn_co.paa",
		"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USarmy\data\BDU_Tropentarn_co.paa",
		"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USarmy\data\BDU_Tropentarn_co.paa"
	};
	class ItemInfo: UniformItem
	{
		uniformModel = "-";
		uniformClass = CUP_B_GER_Soldier_BDU_Tropentarn;
		containerClass = Supply40;
		mass = 20;
	};
};
class CUP_U_B_BAF_BDU_DPM: CUP_U_B_US_BDU
{
	CUP_HEADER_PROTECTED;
	displayName = "BDU (DPM)";
	picture = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\data\ui\gear_u_b_bdu_dpm_ca.paa";
	hiddenSelections[] = {"camo", "camo1", "camo2"};
	hiddenSelectionsTextures[] = {
		"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USarmy\data\BDU_DPM_CO.paa",
		"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USarmy\data\BDU_DPM_CO.paa",
		"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USarmy\data\BDU_DPM_CO.paa"
	};
	class ItemInfo: UniformItem
	{
		uniformModel = "-";
		uniformClass = CUP_B_BAF_Soldier_BDU_DPM;
		containerClass = Supply40;
		mass = 20;
	};
};
class CUP_U_B_BAF_BDU_DPM_ODBottom: CUP_U_B_US_BDU
{
	CUP_HEADER_PROTECTED;
	displayName = "BDU (DPM/OD)";
	picture = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\data\ui\gear_u_b_bdu_dpm_od_ca.paa";
	hiddenSelections[] = {"camo", "camo1", "camo2"};
	hiddenSelectionsTextures[] = {
		"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USarmy\data\US_BDU_OD_CO.paa",
		"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USarmy\data\BDU_DPM_CO.paa",
		"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USarmy\data\BDU_DPM_CO.paa"
	};
	class ItemInfo: UniformItem
	{
		uniformModel = "-";
		uniformClass = CUP_B_BAF_Soldier_BDU_DPM_ODBottom;
		containerClass = Supply40;
		mass = 20;
	};
};
class CUP_U_B_US_BDU_roll : ItemCore
{
	CUP_HEADER_PROTECTED;
	allowedSlots[] = { BACKPACK_SLOT };
	displayName = "BDU (Rolled up)"; /// how would the stuff be displayed in inventory and on ground
	picture = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USMC\data\ui\icon_u_b_usmc_pilotoverall_ca.paa";
	model = "\A3\Characters_F\Common\Suitpacks\suitpack_universal_F.p3d"; /// how does the uniform look when put on ground
	hiddenSelections[] = {"camo", "camo1", "camo2"};
	hiddenSelectionsTextures[] = {
		"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USarmy\data\US_BDU_CO.paa",
		"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USarmy\data\US_BDU_CO.paa",
		"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USarmy\data\US_BDU_CO.paa"
	};
	class ItemInfo: UniformItem
	{
		uniformModel = "-";
		uniformClass = CUP_B_USArmy_Soldier_BDU_roll;
		containerClass = Supply40;
		mass = 20;
	};
};
class CUP_U_B_US_BDU_roll2 : ItemCore
{
	CUP_HEADER_PROTECTED;
	allowedSlots[] = { BACKPACK_SLOT };
	displayName = "BDU (Rolled up 2)"; /// how would the stuff be displayed in inventory and on ground
	picture = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USMC\data\ui\icon_u_b_usmc_pilotoverall_ca.paa";
	model = "\A3\Characters_F\Common\Suitpacks\suitpack_universal_F.p3d"; /// how does the uniform look when put on ground
	hiddenSelections[] = {"camo", "camo1", "camo2"};
	hiddenSelectionsTextures[] = {
		"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USarmy\data\US_BDU_CO.paa",
		"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USarmy\data\US_BDU_CO.paa",
		"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USarmy\data\US_BDU_CO.paa"
	};
	class ItemInfo: UniformItem
	{
		uniformModel = "-";
		uniformClass = CUP_B_USArmy_Soldier_BDU_roll2;
		containerClass = Supply40;
		mass = 20;
	};
};
class CUP_U_B_US_BDU_roll_glove : ItemCore
{
	CUP_HEADER_PROTECTED;
	allowedSlots[] = { BACKPACK_SLOT };
	displayName = "BDU (Rolled, gloves)"; /// how would the stuff be displayed in inventory and on ground
	picture = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USMC\data\ui\icon_u_b_usmc_pilotoverall_ca.paa";
	model = "\A3\Characters_F\Common\Suitpacks\suitpack_universal_F.p3d"; /// how does the uniform look when put on ground
	hiddenSelections[] = {"camo", "camo1", "camo2", "camo3"};
	hiddenSelectionsTextures[] = {
		"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USarmy\data\US_BDU_CO.paa",
		"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USarmy\data\US_BDU_CO.paa",
		"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USarmy\data\US_BDU_CO.paa",
		"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_Russia\data\oakley_co.paa"
	};
	class ItemInfo: UniformItem
	{
		uniformModel = "-";
		uniformClass = CUP_B_USArmy_Soldier_BDU_roll_glove;
		containerClass = Supply40;
		mass = 20;
	};
};
class CUP_U_B_US_BDU_roll2_glove : ItemCore
{
	CUP_HEADER_PROTECTED;
	allowedSlots[] = { BACKPACK_SLOT };
	displayName = "BDU (Rolled 2, gloves)"; /// how would the stuff be displayed in inventory and on ground
	picture = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USMC\data\ui\icon_u_b_usmc_pilotoverall_ca.paa";
	model = "\A3\Characters_F\Common\Suitpacks\suitpack_universal_F.p3d"; /// how does the uniform look when put on ground
	hiddenSelections[] = {"camo", "camo1", "camo2", "camo3"};
	hiddenSelectionsTextures[] = {
		"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USarmy\data\US_BDU_CO.paa",
		"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USarmy\data\US_BDU_CO.paa",
		"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USarmy\data\US_BDU_CO.paa",
		"\CUP\Creatures\People\Military\CUP_Creatures_People_Military_Russia\data\oakley_co.paa"
	};
	class ItemInfo: UniformItem
	{
		uniformModel = "-";
		uniformClass = CUP_B_USArmy_Soldier_BDU_roll2_glove;
		containerClass = Supply40;
		mass = 20;
	};
};
//Crye G3 Uniforms
class CUP_U_CRYE_V1_Full : CUP_U_B_US_BDU
{
	CUP_HEADER_PUBLIC;
    picture = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\data\ui\icon_CUP_CRYE_V1_Full.paa";
	displayName = "Crye Multicam Full";
	allowedSlots[] = { BACKPACK_SLOT };
	model = "\A3\Characters_F\Common\Suitpacks\suitpack_universal_F.p3d";
	hiddenSelections[] = {"Camo", "insignia"};
	hiddenSelectionsTextures[] = {"CUP\Creatures\People\Military\CUP_Creatures_People_Military_USarmy\data\delta\crye_mcam_v1_co.paa"};
	class ItemInfo: UniformItem
	{
		uniformModel = "-";
		uniformClass = "CUP_CRYE_V1_Full";
		containerClass = "Supply40";
		mass = 20;
	};
};
class CUP_U_CRYE_V2_Full : CUP_U_B_US_BDU
{
	CUP_HEADER_PUBLIC;
    picture = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\data\ui\icon_CUP_CRYE_V1_Full.paa";
	displayName = "Crye Multicam Full II";
	allowedSlots[] = { BACKPACK_SLOT };
	model = "\A3\Characters_F\Common\Suitpacks\suitpack_universal_F.p3d";
	hiddenSelections[] = {"Camo", "insignia"};
	hiddenSelectionsTextures[] = {"CUP\Creatures\People\Military\CUP_Creatures_People_Military_USarmy\data\delta\crye_mcam_v2_co.paa"};
	class ItemInfo: UniformItem
	{
		uniformModel = "-";
		uniformClass = "CUP_CRYE_V2_Full";
		containerClass = "Supply40";
		mass = 20;
	};
};
class CUP_U_CRYE_V3_Full : CUP_U_B_US_BDU
{
	CUP_HEADER_PUBLIC;
    picture = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\data\ui\icon_CUP_CRYE_V1_Full.paa";
	displayName = "Crye Multicam Full III";
	allowedSlots[] = { BACKPACK_SLOT };
	model = "\A3\Characters_F\Common\Suitpacks\suitpack_universal_F.p3d";
	hiddenSelections[] = {"Camo", "insignia"};
	hiddenSelectionsTextures[] = {"CUP\Creatures\People\Military\CUP_Creatures_People_Military_USarmy\data\delta\crye_mcam_v3_co.paa"};
	class ItemInfo: UniformItem
	{
		uniformModel = "-";
		uniformClass = "CUP_CRYE_V3_Full";
		containerClass = "Supply40";
		mass = 20;
	};
};
class CUP_U_CRYE_RGR_Full : CUP_U_B_US_BDU
{
	CUP_HEADER_PUBLIC;
    picture = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\data\ui\icon_CUP_CRYE_V1_Full.paa";
	displayName = "Crye Ranger Green Full";
	allowedSlots[] = { BACKPACK_SLOT };
	model = "\A3\Characters_F\Common\Suitpacks\suitpack_universal_F.p3d";
	hiddenSelections[] = {"Camo", "insignia"};
	hiddenSelectionsTextures[] = {"CUP\Creatures\People\Military\CUP_Creatures_People_Military_USarmy\data\delta\crye_g3_rgr_co.paa"};
	class ItemInfo: UniformItem
	{
		uniformModel = "-";
		uniformClass = "CUP_CRYE_RGR_Full";
		containerClass = "Supply40";
		mass = 20;
	};
};
class CUP_U_CRYE_RGR_US_Full : CUP_U_B_US_BDU
{
	CUP_HEADER_PUBLIC;
    picture = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\data\ui\icon_CUP_CRYE_V1_Full.paa";
	displayName = "Crye Ranger Green US Full";
	allowedSlots[] = { BACKPACK_SLOT };
	model = "\A3\Characters_F\Common\Suitpacks\suitpack_universal_F.p3d";
	hiddenSelections[] = {"Camo", "insignia"};
	hiddenSelectionsTextures[] = {"CUP\Creatures\People\Military\CUP_Creatures_People_Military_USarmy\data\delta\crye_g3_rgr_US_co.paa"};
	class ItemInfo: UniformItem
	{
		uniformModel = "-";
		uniformClass = "CUP_CRYE_RGR_US_Full";
		containerClass = "Supply40";
		mass = 20;
	};
};
class CUP_U_CRYE_RGR_Roll : CUP_U_B_US_BDU
{
	CUP_HEADER_PUBLIC;
    picture = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\data\ui\icon_CUP_CRYE_V1_Full.paa";
	displayName = "Crye Ranger Green Rolled";
	allowedSlots[] = { BACKPACK_SLOT };
	model = "\A3\Characters_F\Common\Suitpacks\suitpack_universal_F.p3d";
	hiddenSelections[] = {"Camo", "insignia"};
	hiddenSelectionsTextures[] = {"CUP\Creatures\People\Military\CUP_Creatures_People_Military_USarmy\data\delta\crye_g3_rgr_co.paa"};
	class ItemInfo: UniformItem
	{
		uniformModel = "-";
		uniformClass = "CUP_CRYE_RGR_Roll";
		containerClass = "Supply40";
		mass = 20;
	};
};
class CUP_U_CRYE_RGR_US_Roll : CUP_U_B_US_BDU
{
	CUP_HEADER_PUBLIC;
    picture = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\data\ui\icon_CUP_CRYE_V1_Full.paa";
	displayName = "Crye Ranger Green US Rolled";
	allowedSlots[] = { BACKPACK_SLOT };
	model = "\A3\Characters_F\Common\Suitpacks\suitpack_universal_F.p3d";
	hiddenSelections[] = {"Camo", "insignia"};
	hiddenSelectionsTextures[] = {"CUP\Creatures\People\Military\CUP_Creatures_People_Military_USarmy\data\delta\crye_g3_rgr_US_co.paa"};
	class ItemInfo: UniformItem
	{
		uniformModel = "-";
		uniformClass = "CUP_CRYE_RGR_US_Roll";
		containerClass = "Supply40";
		mass = 20;
	};
};
class CUP_U_CRYE_ATACSFG_Full : CUP_U_B_US_BDU
{
	CUP_HEADER_PUBLIC;
    picture = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\data\ui\icon_CUP_CRYE_V1_Full.paa";
	displayName = "Crye ATACS-FG Full";
	allowedSlots[] = { BACKPACK_SLOT };
	model = "\A3\Characters_F\Common\Suitpacks\suitpack_universal_F.p3d";
	hiddenSelections[] = {"Camo", "insignia"};
	hiddenSelectionsTextures[] = {"CUP\Creatures\People\Military\CUP_Creatures_People_Military_USarmy\data\delta\crye_g3_atacsfg_co.paa"};
	class ItemInfo: UniformItem
	{
		uniformModel = "-";
		uniformClass = "CUP_CRYE_ATACSFG_Full";
		containerClass = "Supply40";
		mass = 20;
	};
};
class CUP_U_CRYE_ATACSFG_Roll : CUP_U_B_US_BDU
{
	CUP_HEADER_PUBLIC;
    picture = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\data\ui\icon_CUP_CRYE_V1_Full.paa";
	displayName = "Crye ATACS-FG Rolled";
	allowedSlots[] = { BACKPACK_SLOT };
	model = "\A3\Characters_F\Common\Suitpacks\suitpack_universal_F.p3d";
	hiddenSelections[] = {"Camo", "insignia"};
	hiddenSelectionsTextures[] = {"CUP\Creatures\People\Military\CUP_Creatures_People_Military_USarmy\data\delta\crye_g3_atacsfg_co.paa"};
	class ItemInfo: UniformItem
	{
		uniformModel = "-";
		uniformClass = "CUP_CRYE_ATACSFG_Roll";
		containerClass = "Supply40";
		mass = 20;
	};
};
class CUP_U_CRYE_ATACSAU_Full : CUP_U_B_US_BDU
{
	CUP_HEADER_PUBLIC;
    picture = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\data\ui\icon_CUP_CRYE_V1_Full.paa";
	displayName = "Crye ATACS-AU Full";
	allowedSlots[] = { BACKPACK_SLOT };
	model = "\A3\Characters_F\Common\Suitpacks\suitpack_universal_F.p3d";
	hiddenSelections[] = {"Camo", "insignia"};
	hiddenSelectionsTextures[] = {"CUP\Creatures\People\Military\CUP_Creatures_People_Military_USarmy\data\delta\crye_g3_atacsau_co.paa"};
	class ItemInfo: UniformItem
	{
		uniformModel = "-";
		uniformClass = "CUP_CRYE_ATACSAU_Full";
		containerClass = "Supply40";
		mass = 20;
	};
};
class CUP_U_CRYE_ATACSAU_Roll : CUP_U_B_US_BDU
{
	CUP_HEADER_PUBLIC;
    picture = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\data\ui\icon_CUP_CRYE_V1_Full.paa";
	displayName = "Crye ATACS-AU Rolled";
	allowedSlots[] = { BACKPACK_SLOT };
	model = "\A3\Characters_F\Common\Suitpacks\suitpack_universal_F.p3d";
	hiddenSelections[] = {"Camo", "insignia"};
	hiddenSelectionsTextures[] = {"CUP\Creatures\People\Military\CUP_Creatures_People_Military_USarmy\data\delta\crye_g3_atacsau_co.paa"};
	class ItemInfo: UniformItem
	{
		uniformModel = "-";
		uniformClass = "CUP_CRYE_ATACSAU_Roll";
		containerClass = "Supply40";
		mass = 20;
	};
};
class CUP_U_CRYE_BLK_Full : CUP_U_B_US_BDU
{
	CUP_HEADER_PUBLIC;
    picture = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\data\ui\icon_CUP_CRYE_V1_Full.paa";
	displayName = "Crye Black Full";
	allowedSlots[] = { BACKPACK_SLOT };
	model = "\A3\Characters_F\Common\Suitpacks\suitpack_universal_F.p3d";
	hiddenSelections[] = {"Camo", "insignia"};
	hiddenSelectionsTextures[] = {"CUP\Creatures\People\Military\CUP_Creatures_People_Military_USarmy\data\delta\crye_g3_blk_co.paa"};
	class ItemInfo: UniformItem
	{
		uniformModel = "-";
		uniformClass = "CUP_CRYE_BLK_Full";
		containerClass = "Supply40";
		mass = 20;
	};
};
class CUP_U_CRYE_BLK_Roll : CUP_U_B_US_BDU
{
	CUP_HEADER_PUBLIC;
    picture = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\data\ui\icon_CUP_CRYE_V1_Full.paa";
	displayName = "Crye Black Rolled";
	allowedSlots[] = { BACKPACK_SLOT };
	model = "\A3\Characters_F\Common\Suitpacks\suitpack_universal_F.p3d";
	hiddenSelections[] = {"Camo", "insignia"};
	hiddenSelectionsTextures[] = {"CUP\Creatures\People\Military\CUP_Creatures_People_Military_USarmy\data\delta\crye_g3_blk_co.paa"};
	class ItemInfo: UniformItem
	{
		uniformModel = "-";
		uniformClass = "CUP_CRYE_BLK_Roll";
		containerClass = "Supply40";
		mass = 20;
	};
};
class CUP_U_CRYE_BLK_RUS_Full : CUP_U_B_US_BDU
{
	CUP_HEADER_PUBLIC;
    picture = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\data\ui\icon_CUP_CRYE_V1_Full.paa";
	displayName = "Crye Black Russia Full";
	allowedSlots[] = { BACKPACK_SLOT };
	model = "\A3\Characters_F\Common\Suitpacks\suitpack_universal_F.p3d";
	hiddenSelections[] = {"Camo", "insignia"};
	hiddenSelectionsTextures[] = {"CUP\Creatures\People\Military\CUP_Creatures_People_Military_USarmy\data\delta\crye_blk_rus_co.paa"};
	class ItemInfo: UniformItem
	{
		uniformModel = "-";
		uniformClass = "CUP_CRYE_BLK_RUS_Full";
		containerClass = "Supply40";
		mass = 20;
	};
};
class CUP_U_CRYE_BLK_RUS_Roll : CUP_U_B_US_BDU
{
	CUP_HEADER_PUBLIC;
    picture = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\data\ui\icon_CUP_CRYE_V1_Full.paa";
	displayName = "Crye Black Russia Rolled";
	allowedSlots[] = { BACKPACK_SLOT };
	model = "\A3\Characters_F\Common\Suitpacks\suitpack_universal_F.p3d";
	hiddenSelections[] = {"Camo", "insignia"};
	hiddenSelectionsTextures[] = {"CUP\Creatures\People\Military\CUP_Creatures_People_Military_USarmy\data\delta\crye_blk_rus_co.paa"};
	class ItemInfo: UniformItem
	{
		uniformModel = "-";
		uniformClass = "CUP_CRYE_BLK_RUS_Roll";
		containerClass = "Supply40";
		mass = 20;
	};
};
class CUP_U_CRYE_MCAM_RUS_Full : CUP_U_B_US_BDU
{
	CUP_HEADER_PUBLIC;
    picture = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\data\ui\icon_CUP_CRYE_V1_Full.paa";
	displayName = "Crye MCam v1 Russia Full";
	allowedSlots[] = { BACKPACK_SLOT };
	model = "\A3\Characters_F\Common\Suitpacks\suitpack_universal_F.p3d";
	hiddenSelections[] = {"Camo", "insignia"};
	hiddenSelectionsTextures[] = {"CUP\Creatures\People\Military\CUP_Creatures_People_Military_USarmy\data\delta\crye_mcam_rus_co.paa"};
	class ItemInfo: UniformItem
	{
		uniformModel = "-";
		uniformClass = "CUP_CRYE_MCAM_RUS_Full";
		containerClass = "Supply40";
		mass = 20;
	};
};
class CUP_U_CRYE_MCAM_RUS_Roll : CUP_U_B_US_BDU
{
	CUP_HEADER_PUBLIC;
    picture = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\data\ui\icon_CUP_CRYE_V1_Full.paa";
	displayName = "Crye MCam v1 Russia Rolled";
	allowedSlots[] = { BACKPACK_SLOT };
	model = "\A3\Characters_F\Common\Suitpacks\suitpack_universal_F.p3d";
	hiddenSelections[] = {"Camo", "insignia"};
	hiddenSelectionsTextures[] = {"CUP\Creatures\People\Military\CUP_Creatures_People_Military_USarmy\data\delta\crye_mcam_rus_co.paa"};
	class ItemInfo: UniformItem
	{
		uniformModel = "-";
		uniformClass = "CUP_CRYE_MCAM_RUS_Roll";
		containerClass = "Supply40";
		mass = 20;
	};
};
class CUP_U_CRYE_MCAM_RUS2_Full : CUP_U_B_US_BDU
{
	CUP_HEADER_PUBLIC;
    picture = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\data\ui\icon_CUP_CRYE_V1_Full.paa";
	displayName = "Crye MCam v2 Russia Full";
	allowedSlots[] = { BACKPACK_SLOT };
	model = "\A3\Characters_F\Common\Suitpacks\suitpack_universal_F.p3d";
	hiddenSelections[] = {"Camo", "insignia"};
	hiddenSelectionsTextures[] = {"CUP\Creatures\People\Military\CUP_Creatures_People_Military_USarmy\data\delta\crye_mcam_rus2_co.paa"};
	class ItemInfo: UniformItem
	{
		uniformModel = "-";
		uniformClass = "CUP_CRYE_MCAM_RUS2_Full";
		containerClass = "Supply40";
		mass = 20;
	};
};
class CUP_U_CRYE_MCAM_RUS2_Roll : CUP_U_B_US_BDU
{
	CUP_HEADER_PUBLIC;
    picture = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\data\ui\icon_CUP_CRYE_V1_Full.paa";
	displayName = "Crye MCam v2 Russia Rolled";
	allowedSlots[] = { BACKPACK_SLOT };
	model = "\A3\Characters_F\Common\Suitpacks\suitpack_universal_F.p3d";
	hiddenSelections[] = {"Camo", "insignia"};
	hiddenSelectionsTextures[] = {"CUP\Creatures\People\Military\CUP_Creatures_People_Military_USarmy\data\delta\crye_mcam_rus2_co.paa"};
	class ItemInfo: UniformItem
	{
		uniformModel = "-";
		uniformClass = "CUP_CRYE_MCAM_RUS2_Roll";
		containerClass = "Supply40";
		mass = 20;
	};
};
class CUP_U_CRYE_MCAM_NP_Full : CUP_U_B_US_BDU
{
	CUP_HEADER_PUBLIC;
    picture = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\data\ui\icon_CUP_CRYE_V1_Full.paa";
	displayName = "Crye MCam v1 Patchless Full";
	allowedSlots[] = { BACKPACK_SLOT };
	model = "\A3\Characters_F\Common\Suitpacks\suitpack_universal_F.p3d";
	hiddenSelections[] = {"Camo", "insignia"};
	hiddenSelectionsTextures[] = {"CUP\Creatures\People\Military\CUP_Creatures_People_Military_USarmy\data\delta\crye_mcam_patchless_co.paa"};
	class ItemInfo: UniformItem
	{
		uniformModel = "-";
		uniformClass = "CUP_CRYE_MCAM_NP_Full";
		containerClass = "Supply40";
		mass = 20;
	};
};
class CUP_U_CRYE_MCAM_NP_Roll : CUP_U_B_US_BDU
{
	CUP_HEADER_PUBLIC;
    picture = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\data\ui\icon_CUP_CRYE_V1_Full.paa";
	displayName = "Crye MCam v1 Patchless Rolled";
	allowedSlots[] = { BACKPACK_SLOT };
	model = "\A3\Characters_F\Common\Suitpacks\suitpack_universal_F.p3d";
	hiddenSelections[] = {"Camo", "insignia"};
	hiddenSelectionsTextures[] = {"CUP\Creatures\People\Military\CUP_Creatures_People_Military_USarmy\data\delta\crye_mcam_patchless_co.paa"};
	class ItemInfo: UniformItem
	{
		uniformModel = "-";
		uniformClass = "CUP_CRYE_MCAM_NP_Roll";
		containerClass = "Supply40";
		mass = 20;
	};
};
class CUP_U_CRYE_MCAM_NP2_Full : CUP_U_B_US_BDU
{
	CUP_HEADER_PUBLIC;
    picture = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\data\ui\icon_CUP_CRYE_V1_Full.paa";
	displayName = "Crye MCam v2 Patchless Full";
	allowedSlots[] = { BACKPACK_SLOT };
	model = "\A3\Characters_F\Common\Suitpacks\suitpack_universal_F.p3d";
	hiddenSelections[] = {"Camo", "insignia"};
	hiddenSelectionsTextures[] = {"CUP\Creatures\People\Military\CUP_Creatures_People_Military_USarmy\data\delta\crye_mcam_patchless2_co.paa"};
	class ItemInfo: UniformItem
	{
		uniformModel = "-";
		uniformClass = "CUP_CRYE_MCAM_NP2_Full";
		containerClass = "Supply40";
		mass = 20;
	};
};
class CUP_U_CRYE_MCAM_NP2_Roll : CUP_U_B_US_BDU
{
	CUP_HEADER_PUBLIC;
    picture = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\data\ui\icon_CUP_CRYE_V1_Full.paa";
	displayName = "Crye MCam v2 Patchless Rolled";
	allowedSlots[] = { BACKPACK_SLOT };
	model = "\A3\Characters_F\Common\Suitpacks\suitpack_universal_F.p3d";
	hiddenSelections[] = {"Camo", "insignia"};
	hiddenSelectionsTextures[] = {"CUP\Creatures\People\Military\CUP_Creatures_People_Military_USarmy\data\delta\crye_mcam_patchless2_co.paa"};
	class ItemInfo: UniformItem
	{
		uniformModel = "-";
		uniformClass = "CUP_CRYE_MCAM_NP2_Roll";
		containerClass = "Supply40";
		mass = 20;
	};
};
class CUP_U_CRYE_TAN_Full : CUP_U_B_US_BDU
{
	CUP_HEADER_PUBLIC;
    picture = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\data\ui\icon_CUP_CRYE_V1_Full.paa";
	displayName = "Crye Tan Full";
	allowedSlots[] = { BACKPACK_SLOT };
	model = "\A3\Characters_F\Common\Suitpacks\suitpack_universal_F.p3d";
	hiddenSelections[] = {"Camo", "insignia"};
	hiddenSelectionsTextures[] = {"CUP\Creatures\People\Military\CUP_Creatures_People_Military_USarmy\data\delta\crye_g3_tan_co.paa"};
	class ItemInfo: UniformItem
	{
		uniformModel = "-";
		uniformClass = "CUP_CRYE_TAN_Full";
		containerClass = "Supply40";
		mass = 20;
	};
};
class CUP_U_CRYE_TAN_Roll : CUP_U_B_US_BDU
{
	CUP_HEADER_PUBLIC;
    picture = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\data\ui\icon_CUP_CRYE_V1_Full.paa";
	displayName = "Crye Tan Rolled";
	allowedSlots[] = { BACKPACK_SLOT };
	model = "\A3\Characters_F\Common\Suitpacks\suitpack_universal_F.p3d";
	hiddenSelections[] = {"Camo", "insignia"};
	hiddenSelectionsTextures[] = {"CUP\Creatures\People\Military\CUP_Creatures_People_Military_USarmy\data\delta\crye_g3_tan_co.paa"};
	class ItemInfo: UniformItem
	{
		uniformModel = "-";
		uniformClass = "CUP_CRYE_TAN_Roll";
		containerClass = "Supply40";
		mass = 20;
	};
};
class CUP_U_CRYE_TAN_US_Full : CUP_U_B_US_BDU
{
	CUP_HEADER_PUBLIC;
    picture = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\data\ui\icon_CUP_CRYE_V1_Full.paa";
	displayName = "Crye Tan US Full";
	allowedSlots[] = { BACKPACK_SLOT };
	model = "\A3\Characters_F\Common\Suitpacks\suitpack_universal_F.p3d";
	hiddenSelections[] = {"Camo", "insignia"};
	hiddenSelectionsTextures[] = {"CUP\Creatures\People\Military\CUP_Creatures_People_Military_USarmy\data\delta\crye_g3_tan_US_co.paa"};
	class ItemInfo: UniformItem
	{
		uniformModel = "-";
		uniformClass = "CUP_CRYE_TAN_US_Full";
		containerClass = "Supply40";
		mass = 20;
	};
};
class CUP_U_CRYE_TAN_US_Roll : CUP_U_B_US_BDU
{
	CUP_HEADER_PUBLIC;
    picture = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\data\ui\icon_CUP_CRYE_V1_Full.paa";
	displayName = "Crye Tan US Rolled";
	allowedSlots[] = { BACKPACK_SLOT };
	model = "\A3\Characters_F\Common\Suitpacks\suitpack_universal_F.p3d";
	hiddenSelections[] = {"Camo", "insignia"};
	hiddenSelectionsTextures[] = {"CUP\Creatures\People\Military\CUP_Creatures_People_Military_USarmy\data\delta\crye_g3_tan_US_co.paa"};
	class ItemInfo: UniformItem
	{
		uniformModel = "-";
		uniformClass = "CUP_CRYE_TAN_US_Roll";
		containerClass = "Supply40";
		mass = 20;
	};
};
class CUP_U_CRYE_V1_Roll : CUP_U_B_US_BDU
{
	CUP_HEADER_PUBLIC;
    picture = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\data\ui\icon_CUP_CRYE_V1_Full.paa";
	displayName = "Crye Multicam Rolled";
	allowedSlots[] = { BACKPACK_SLOT };
	model = "\A3\Characters_F\Common\Suitpacks\suitpack_universal_F.p3d";
	hiddenSelections[] = {"Camo", "insignia"};
	hiddenSelectionsTextures[] = {"CUP\Creatures\People\Military\CUP_Creatures_People_Military_USarmy\data\delta\crye_mcam_v1_co.paa"};
	class ItemInfo: UniformItem
	{
		uniformModel = "-";
		uniformClass = "CUP_CRYE_V1_Roll";
		containerClass = "Supply40";
		mass = 20;
	};
};
class CUP_U_CRYE_V2_Roll : CUP_U_B_US_BDU
{
	CUP_HEADER_PUBLIC;
    picture = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\data\ui\icon_CUP_CRYE_V1_Full.paa";
	displayName = "Crye Multicam Rolled II";
	allowedSlots[] = { BACKPACK_SLOT };
	model = "\A3\Characters_F\Common\Suitpacks\suitpack_universal_F.p3d";
	hiddenSelections[] = {"Camo", "insignia"};
	hiddenSelectionsTextures[] = {"CUP\Creatures\People\Military\CUP_Creatures_People_Military_USarmy\data\delta\crye_mcam_v2_co.paa"};
	class ItemInfo: UniformItem
	{
		uniformModel = "-";
		uniformClass = "CUP_CRYE_V2_Roll";
		containerClass = "Supply40";
		mass = 20;
	};
};
class CUP_U_CRYE_V3_Roll : CUP_U_B_US_BDU
{
	CUP_HEADER_PUBLIC;
    picture = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\data\ui\icon_CUP_CRYE_V1_Full.paa";
	displayName = "Crye Multicam Rolled III";
	allowedSlots[] = { BACKPACK_SLOT };
	model = "\A3\Characters_F\Common\Suitpacks\suitpack_universal_F.p3d";
	hiddenSelections[] = {"Camo", "insignia"};
	hiddenSelectionsTextures[] = {"CUP\Creatures\People\Military\CUP_Creatures_People_Military_USarmy\data\delta\crye_mcam_v3_co.paa"};
	class ItemInfo: UniformItem
	{
		uniformModel = "-";
		uniformClass = "CUP_CRYE_V3_Roll";
		containerClass = "Supply40";
		mass = 20;
	};
};
class CUP_U_CRYEG3_V1 : CUP_U_B_US_BDU
{
	CUP_HEADER_PUBLIC;
    picture = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\data\ui\icon_CUP_CRYE_V1_Full.paa";
	displayName = "Crye G3AW Coyote";
	allowedSlots[] = { BACKPACK_SLOT };
	model = "\A3\Characters_F\Common\Suitpacks\suitpack_universal_F.p3d";
	hiddenSelections[] = {"Camo", "insignia"};
	hiddenSelectionsTextures[] = {"CUP\Creatures\People\Military\CUP_Creatures_People_Military_USarmy\data\delta\crye_g3_v1_co.paa"};
	class ItemInfo: UniformItem
	{
		uniformModel = "-";
		uniformClass = "CUP_CRYEG3_V1";
		containerClass = "Supply40";
		mass = 20;
	};
};
class CUP_U_CRYEG3_V2 : CUP_U_B_US_BDU
{
	CUP_HEADER_PUBLIC;
    picture = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\data\ui\icon_CUP_CRYE_V1_Full.paa";
	displayName = "Crye G3AW Khaki";
	allowedSlots[] = { BACKPACK_SLOT };
	model = "\A3\Characters_F\Common\Suitpacks\suitpack_universal_F.p3d";
	hiddenSelections[] = {"Camo", "insignia"};
	hiddenSelectionsTextures[] = {"CUP\Creatures\People\Military\CUP_Creatures_People_Military_USarmy\data\delta\crye_g3_v2_co.paa"};
	class ItemInfo: UniformItem
	{
		uniformModel = "-";
		uniformClass = "CUP_CRYEG3_V2";
		containerClass = "Supply40";
		mass = 20;
	};
};

//MARSOC G3 CRYES
class CUP_U_CRYEG3_MARSOC_V1 : CUP_U_B_US_BDU
{
	CUP_HEADER_PROTECTED;
    picture = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\data\ui\icon_CUP_CRYE_V1_Full.paa";
	displayName = "Crye G3 M81 (MARSOC)";
	allowedSlots[] = { BACKPACK_SLOT };
	model = "\A3\Characters_F\Common\Suitpacks\suitpack_universal_F.p3d";
	hiddenSelections[] = {"Camo", "insignia"};
	hiddenSelectionsTextures[] = {"CUP\Creatures\People\Military\CUP_Creatures_People_Military_USarmy\data\delta\crye_g3_m81_co.paa","CUP\Creatures\People\Military\CUP_Creatures_People_Military_USarmy\data\delta\raiderblue_co.paa"};
	class ItemInfo: UniformItem
	{
		uniformModel = "-";
		uniformClass = "CUP_CRYEG3_MARSOC_V1";
		containerClass = "Supply40";
		mass = 20;
	};
};
class CUP_U_CRYEG3_MARSOC_V1_Roll : CUP_U_B_US_BDU
{
	CUP_HEADER_PROTECTED;
    picture = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\data\ui\icon_CUP_CRYE_V1_Full.paa";
	displayName = "Crye G3 M81 Rolled (MARSOC)";
	allowedSlots[] = { BACKPACK_SLOT };
	model = "\A3\Characters_F\Common\Suitpacks\suitpack_universal_F.p3d";
	hiddenSelections[] = {"Camo", "insignia"};
	hiddenSelectionsTextures[] = {"CUP\Creatures\People\Military\CUP_Creatures_People_Military_USarmy\data\delta\crye_g3_m81_co.paa","CUP\Creatures\People\Military\CUP_Creatures_People_Military_USarmy\data\delta\marine_raiders_alt_ca.paa"};
	class ItemInfo: UniformItem
	{
		uniformModel = "-";
		uniformClass = "CUP_CRYEG3_MARSOC_V1_Roll";
		containerClass = "Supply40";
		mass = 20;
	};
};
class CUP_U_CRYEG3_MARSOC_V2 : CUP_U_B_US_BDU
{
	CUP_HEADER_PROTECTED;
    picture = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\data\ui\icon_CUP_CRYE_V1_Full.paa";
	displayName = "Crye G3 M81/Grey (MARSOC)";
	allowedSlots[] = { BACKPACK_SLOT };
	model = "\A3\Characters_F\Common\Suitpacks\suitpack_universal_F.p3d";
	hiddenSelections[] = {"Camo", "insignia"};
	hiddenSelectionsTextures[] = {"CUP\Creatures\People\Military\CUP_Creatures_People_Military_USarmy\data\delta\crye_g3_m81_grey_co.paa","CUP\Creatures\People\Military\CUP_Creatures_People_Military_USarmy\data\delta\marine_raiders_grn_ca.paa"};
	class ItemInfo: UniformItem
	{
		uniformModel = "-";
		uniformClass = "CUP_CRYEG3_MARSOC_V2";
		containerClass = "Supply40";
		mass = 20;
	};
};
class CUP_U_CRYEG3_MARSOC_V2_Roll : CUP_U_B_US_BDU
{
	CUP_HEADER_PROTECTED;
    picture = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\data\ui\icon_CUP_CRYE_V1_Full.paa";
	displayName = "Crye G3 M81/Grey Rolled (MARSOC)";
	allowedSlots[] = { BACKPACK_SLOT };
	model = "\A3\Characters_F\Common\Suitpacks\suitpack_universal_F.p3d";
	hiddenSelections[] = {"Camo", "insignia"};
	hiddenSelectionsTextures[] = {"CUP\Creatures\People\Military\CUP_Creatures_People_Military_USarmy\data\delta\crye_g3_m81_grey_co.paa","CUP\Creatures\People\Military\CUP_Creatures_People_Military_USarmy\data\delta\marine_raiders_ca.paa"};
	class ItemInfo: UniformItem
	{
		uniformModel = "-";
		uniformClass = "CUP_CRYEG3_MARSOC_V2_Roll";
		containerClass = "Supply40";
		mass = 20;
	};
};
class CUP_U_CRYEG3_MARSOC_V3 : CUP_U_B_US_BDU
{
	CUP_HEADER_PROTECTED;
    picture = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\data\ui\icon_CUP_CRYE_V1_Full.paa";
	displayName = "Crye G3 Grey/M81 (MARSOC)";
	allowedSlots[] = { BACKPACK_SLOT };
	model = "\A3\Characters_F\Common\Suitpacks\suitpack_universal_F.p3d";
	hiddenSelections[] = {"Camo", "insignia"};
	hiddenSelectionsTextures[] = {"CUP\Creatures\People\Military\CUP_Creatures_People_Military_USarmy\data\delta\crye_g3_grey_m81_co.paa","CUP\Creatures\People\Military\CUP_Creatures_People_Military_USarmy\data\delta\marine_raiders_gry_ca.paa"};
	class ItemInfo: UniformItem
	{
		uniformModel = "-";
		uniformClass = "CUP_CRYEG3_MARSOC_V3";
		containerClass = "Supply40";
		mass = 20;
	};
};
class CUP_U_CRYEG3_MARSOC_V3_Roll : CUP_U_B_US_BDU
{
	CUP_HEADER_PROTECTED;
    picture = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\data\ui\icon_CUP_CRYE_V1_Full.paa";
	displayName = "Crye G3 Grey/M81 Rolled (MARSOC)";
	allowedSlots[] = { BACKPACK_SLOT };
	model = "\A3\Characters_F\Common\Suitpacks\suitpack_universal_F.p3d";
	hiddenSelections[] = {"Camo", "insignia"};
	hiddenSelectionsTextures[] = {"CUP\Creatures\People\Military\CUP_Creatures_People_Military_USarmy\data\delta\crye_g3_grey_m81_co.paa","CUP\Creatures\People\Military\CUP_Creatures_People_Military_USarmy\data\delta\marine_raiders_grn_ca.paa"};
	class ItemInfo: UniformItem
	{
		uniformModel = "-";
		uniformClass = "CUP_CRYEG3_MARSOC_V3_Roll";
		containerClass = "Supply40";
		mass = 20;
	};
};
class CUP_U_CRYEG3_MARSOC_V4 : CUP_U_B_US_BDU
{
	CUP_HEADER_PROTECTED;
    picture = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\data\ui\icon_CUP_CRYE_V1_Full.paa";
	displayName = "Crye G3 M81/Green (MARSOC)";
	allowedSlots[] = { BACKPACK_SLOT };
	model = "\A3\Characters_F\Common\Suitpacks\suitpack_universal_F.p3d";
	hiddenSelections[] = {"Camo", "insignia"};
	hiddenSelectionsTextures[] = {"CUP\Creatures\People\Military\CUP_Creatures_People_Military_USarmy\data\delta\crye_g3_m81_green_co.paa","CUP\Creatures\People\Military\CUP_Creatures_People_Military_USarmy\data\delta\raiderblue_co.paa"};
	class ItemInfo: UniformItem
	{
		uniformModel = "-";
		uniformClass = "CUP_CRYEG3_MARSOC_V4";
		containerClass = "Supply40";
		mass = 20;
	};
};
class CUP_U_CRYEG3_MARSOC_V4_Roll : CUP_U_B_US_BDU
{
	CUP_HEADER_PROTECTED;
    picture = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\data\ui\icon_CUP_CRYE_V1_Full.paa";
	displayName = "Crye G3 M81/Green Rolled (MARSOC)";
	allowedSlots[] = { BACKPACK_SLOT };
	model = "\A3\Characters_F\Common\Suitpacks\suitpack_universal_F.p3d";
	hiddenSelections[] = {"Camo", "insignia"};
	hiddenSelectionsTextures[] = {"CUP\Creatures\People\Military\CUP_Creatures_People_Military_USarmy\data\delta\crye_g3_m81_green_co.paa","CUP\Creatures\People\Military\CUP_Creatures_People_Military_USarmy\data\delta\marine_raiders_grn_ca.paa"};
	class ItemInfo: UniformItem
	{
		uniformModel = "-";
		uniformClass = "CUP_CRYEG3_MARSOC_V4_Roll";
		containerClass = "Supply40";
		mass = 20;
	};
};
class CUP_U_CRYEG3_MARSOC_V5 : CUP_U_B_US_BDU
{
	CUP_HEADER_PROTECTED;
    picture = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\data\ui\icon_CUP_CRYE_V1_Full.paa";
	displayName = "Crye G3 Green/M81 (MARSOC)";
	allowedSlots[] = { BACKPACK_SLOT };
	model = "\A3\Characters_F\Common\Suitpacks\suitpack_universal_F.p3d";
	hiddenSelections[] = {"Camo", "insignia"};
	hiddenSelectionsTextures[] = {"CUP\Creatures\People\Military\CUP_Creatures_People_Military_USarmy\data\delta\crye_g3_green_m81_co.paa","CUP\Creatures\People\Military\CUP_Creatures_People_Military_USarmy\data\delta\marine_raiders_grn_ca.paa"};
	class ItemInfo: UniformItem
	{
		uniformModel = "-";
		uniformClass = "CUP_CRYEG3_MARSOC_V5";
		containerClass = "Supply40";
		mass = 20;
	};
};
class CUP_U_CRYEG3_MARSOC_V5_Roll : CUP_U_B_US_BDU
{
	CUP_HEADER_PROTECTED;
    picture = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\data\ui\icon_CUP_CRYE_V1_Full.paa";
	displayName = "Crye G3 Green/M81 Rolled (MARSOC)";
	allowedSlots[] = { BACKPACK_SLOT };
	model = "\A3\Characters_F\Common\Suitpacks\suitpack_universal_F.p3d";
	hiddenSelections[] = {"Camo", "insignia"};
	hiddenSelectionsTextures[] = {"CUP\Creatures\People\Military\CUP_Creatures_People_Military_USarmy\data\delta\crye_g3_green_m81_co.paa","CUP\Creatures\People\Military\CUP_Creatures_People_Military_USarmy\data\delta\marine_raiders_alt_ca.paa"};
	class ItemInfo: UniformItem
	{
		uniformModel = "-";
		uniformClass = "CUP_CRYEG3_MARSOC_V5_Roll";
		containerClass = "Supply40";
		mass = 20;
	};
};
class CUP_U_CRYEG3_MARSOC_V6 : CUP_U_B_US_BDU
{
	CUP_HEADER_PROTECTED;
    picture = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\data\ui\icon_CUP_CRYE_V1_Full.paa";
	displayName = "Crye G3 M81 v2 (MARSOC)";
	allowedSlots[] = { BACKPACK_SLOT };
	model = "\A3\Characters_F\Common\Suitpacks\suitpack_universal_F.p3d";
	hiddenSelections[] = {"Camo", "insignia"};
	hiddenSelectionsTextures[] = {"CUP\Creatures\People\Military\CUP_Creatures_People_Military_USarmy\data\delta\crye_g3_m81_v2_co.paa","CUP\Creatures\People\Military\CUP_Creatures_People_Military_USarmy\data\delta\raiderblue_co.paa"};
	class ItemInfo: UniformItem
	{
		uniformModel = "-";
		uniformClass = "CUP_CRYEG3_MARSOC_V6";
		containerClass = "Supply40";
		mass = 20;
	};
};
class CUP_U_CRYEG3_MARSOC_V6_Roll : CUP_U_B_US_BDU
{
	CUP_HEADER_PROTECTED;
    picture = "\CUP\Creatures\People\Military\CUP_Creatures_People_Military_USArmy\data\ui\icon_CUP_CRYE_V1_Full.paa";
	displayName = "Crye G3 M81 v2 Rolled (MARSOC)";
	allowedSlots[] = { BACKPACK_SLOT };
	model = "\A3\Characters_F\Common\Suitpacks\suitpack_universal_F.p3d";
	hiddenSelections[] = {"Camo", "insignia"};
	hiddenSelectionsTextures[] = {"CUP\Creatures\People\Military\CUP_Creatures_People_Military_USarmy\data\delta\crye_g3_m81_v2_co.paa","CUP\Creatures\People\Military\CUP_Creatures_People_Military_USarmy\data\delta\marine_raiders_alt_ca.paa"};
	class ItemInfo: UniformItem
	{
		uniformModel = "-";
		uniformClass = "CUP_CRYEG3_MARSOC_V6_Roll";
		containerClass = "Supply40";
		mass = 20;
	};
};
