# Clustering settings
config_clustering = c.ClusteringSettings(
    criteria="distance",
    node_types=["O"],
    node_masses=[15.9994],
    connectivity=["O", "O"],
    cutoffs=[c.Cutoff(type1="O", type2="O", distance=3.5)],

    with_coordination_number=True,
    with_alternating=True,
    coordination_mode="same_type", 
    coordination_range=[4,9]
)