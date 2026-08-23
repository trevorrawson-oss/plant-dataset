# CONTROL-METHOD CATALOG -- the ONLY 42 methods a rung may name.
# Ladder order is by tier: cultural < physical < biological < soft_chemical < conventional.

## cultural
  airflow_spacing                applies_to=['bacterial', 'disease_general', 'fungal_foliar']
  avoid_ammoniacal_nitrogen      applies_to=['physiological']
  balance_nitrogen               applies_to=['insect_soft_bodied']
  bottom_watering                applies_to=['bacterial', 'fungal_soilborne', 'insect_general', 'mollusk']
  crop_rotation                  applies_to=['any']
  even_watering                  applies_to=['mite', 'physiological']
  garden_sanitation              applies_to=['any']
  improve_drainage               applies_to=['disease_general', 'fungal_soilborne']
  moisture_buffering_mulch       applies_to=['physiological']
  raise_soil_ph                  applies_to=['fungal_soilborne']
  reflective_mulch               applies_to=['insect_soft_bodied', 'viral']
  resistant_varieties            applies_to=['any']
  sensible_seeding_rate          applies_to=['disease_general', 'fungal_soilborne']
  straw_mulch                    applies_to=['disease_general', 'fungal_foliar']

## physical
  bird_netting                   applies_to=['vertebrate']
  bird_scare_deterrents          applies_to=['vertebrate']
  codling_moth_pheromone_trap    applies_to=['insect_boring', 'insect_general']
  floating_row_cover             applies_to=['any']
  fruit_bagging                  applies_to=['insect_boring', 'insect_general']
  handpick                       applies_to=['insect_chewing', 'insect_general', 'mollusk']
  kaolin_clay                    applies_to=['insect_boring', 'insect_chewing', 'insect_general']
  prune_out_infection            applies_to=['bacterial', 'disease_general']
  red_sphere_trap                applies_to=['insect_general']
  slug_traps_barriers            applies_to=['mollusk']
  soil_solarization              applies_to=['bacterial', 'disease_general', 'fungal_soilborne', 'nematode']
  stem_collars                   applies_to=['insect_chewing', 'insect_general']
  swd_exclusion_netting          applies_to=['insect_general']
  swd_monitoring_traps           applies_to=['insect_general']
  water_spray                    applies_to=['insect_soft_bodied', 'mite']
  yellow_sticky_traps            applies_to=['insect_general', 'insect_soft_bodied']

## biological
  beneficial_nematodes           applies_to=['insect_general']
  beneficial_predators           applies_to=['insect_general', 'insect_soft_bodied']
  bt                             applies_to=['insect_chewing']

## soft_chemical
  copper_fungicide               applies_to=['bacterial', 'disease_general', 'fungal_foliar']
  horticultural_oil              applies_to=['insect_general', 'insect_soft_bodied', 'mite']
  insecticidal_soap              applies_to=['insect_soft_bodied', 'mite']
  iron_phosphate_slug_bait       applies_to=['mollusk']
  neem_oil                       applies_to=['insect_general', 'insect_soft_bodied']
  spinosad                       applies_to=['insect_chewing', 'insect_general']
  sulfur                         applies_to=['disease_general', 'fungal_foliar', 'mite']

## conventional
  carbaryl                       applies_to=['insect_boring', 'insect_chewing', 'insect_general']
  pyrethroid                     applies_to=['insect_boring', 'insect_chewing', 'insect_general', 'insect_soft_bodied']

# problem.type -> applies_to targets that legitimately fit it.
  bacterial       ['bacterial', 'disease_general']
  fungal          ['disease_general', 'fungal_foliar', 'fungal_soilborne']
  insect          ['insect_boring', 'insect_chewing', 'insect_general', 'insect_soft_bodied']
  mite            ['insect_general', 'mite']
  mollusk         ['mollusk']
  nematode        ['nematode']
  physiological   ['physiological']
  vertebrate      ['vertebrate']
  viral           ['disease_general', 'viral']