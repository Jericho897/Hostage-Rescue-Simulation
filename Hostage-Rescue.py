import numpy as np
import matplotlib.pyplot as plt

# Define parameters
num_simulations = 1000
num_hostages = 12
num_hostage_takers = 6

# Define probability distributions based on expert estimates or real-world data
rescue_time_min = 60  # minutes (realistic minimum rescue time)
rescue_time_max = 240  # minutes (realistic maximum rescue time)
hostage_behavior_prob = 0.7  # Hostage compliance based on historical data
hostage_injury_prob = 0.2  # Probability of hostages getting injured    
hostage_taker_injury_prob = 0.3  # Probability of hostage-takers getting injured
hostage_taker_capture_prob = 0.4  # Probability of capturing hostage-takers
hostage_taker_aggressiveness = np.random.beta(3, 5, size=num_simulations)  # Hostage-taker aggressiveness (adjusted parameters)
negotiation_success_prob = np.random.triangular(0.1, 0.3, 0.5, size=num_simulations)  # triangular distribution of negotiation success (adjusted parameters)
terrain_difficulty = np.random.triangular(0.1, 0.5, 0.8, size=num_simulations)  # triangular distribution of terrain difficulty
rescue_team_skill = np.random.triangular(0.3, 0.6, 0.9, size=num_simulations)  # triangular distribution of rescue team skill
negotiation_duration_mean = 90  # minutes (based on negotiation expert opinion)
negotiation_duration_std = 15  # minutes
entry_points_mean = 1.5  # On average, 1.5 entry points
entry_points_std = 0.5
hostage_health_status_mean = 75  # percentage (based on historical data)
hostage_health_status_std = 10  # percentage
hostage_taker_strength_mean = 0.5  # normalized strength (based on SWAT team reports)
hostage_taker_strength_std = 0.2  # normalized strength
communication_reliability_mean = 0.8  # percentage (based on communication equipment reliability)
communication_reliability_std = 0.1  # percentage

# Define parameters for house layout
num_rooms_mean = 6  # Average number of rooms in the house
num_rooms_std = 2   # Standard deviation of number of rooms
num_entry_points_mean = 2  # Average number of entry points into the house
num_entry_points_std = 1   # Standard deviation of number of entry points

# Define raid time window (in minutes from the start of the simulation)
raid_time_window_start = 60  # Start of raid time window
raid_time_window_end = 120  # End of raid time window

# Run simulations
results = []
for i in range(num_simulations):
    # Sample raid time within the raid time window
    raid_time = np.random.randint(raid_time_window_start, raid_time_window_end + 1)

    # Sample from probability distributions
    rescue_time = np.random.uniform(rescue_time_min, rescue_time_max)
    hostages_rescued = np.random.binomial(num_hostages, hostage_behavior_prob)
    hostages_injured = np.random.binomial(hostages_rescued, hostage_injury_prob)  # Number of injured hostages
    hostages_uninjured = hostages_rescued - hostages_injured  # Number of uninjured hostages
    casualties_hostages = np.random.randint(0, int(hostages_uninjured * 0.3) + 1)  # Assume up to 30% casualties among uninjured hostages
    casualties_hostage_takers = np.random.binomial(num_hostage_takers, 1 - hostage_taker_aggressiveness[i])
    hostage_takers_injured = np.random.binomial(num_hostage_takers, hostage_taker_injury_prob)  # Number of injured hostage-takers
    hostage_takers_captured = np.random.binomial(num_hostage_takers, hostage_taker_capture_prob)  # Number of captured hostage-takers
    negotiation_outcome = np.random.binomial(1, negotiation_success_prob[i])
    terrain_modifier = terrain_difficulty[i]
    rescue_team_modifier = rescue_team_skill[i]
    negotiation_duration = max(0, np.random.normal(negotiation_duration_mean, negotiation_duration_std))
    entry_points = max(1, int(np.random.normal(entry_points_mean, entry_points_std)))
    hostage_health_status = max(0, min(100, np.random.normal(hostage_health_status_mean, hostage_health_status_std)))  # Ensure health status is between 0 and 100
    hostage_taker_strength = max(0, min(1, np.random.normal(hostage_taker_strength_mean, hostage_taker_strength_std)))  # Ensure strength is between 0 and 1
    communication_reliability = max(0, min(1, np.random.normal(communication_reliability_mean, communication_reliability_std)))  # Ensure reliability is between 0 and 1
    
    # Sample number of rooms and entry points from normal distributions
    num_rooms = np.random.randint(max(1, num_rooms_mean - num_rooms_std), num_rooms_mean + num_rooms_std + 1)
    num_entry_points = np.random.randint(max(1, num_entry_points_mean - num_entry_points_std), num_entry_points_mean + num_entry_points_std + 1)
    
    # Adjust rescue time based on general terrain and urban terrain difficulty
    rescue_time *= (1 + terrain_modifier) * (1 - rescue_team_modifier) * (1 + num_rooms * 0.05) * (1 + num_entry_points * 0.1)

    # Store raid time along with other results
    results.append({
        'raid_time': raid_time,
        'rescue_time': rescue_time,
        'hostages_rescued': hostages_rescued,
        'hostages_injured': hostages_injured,
        'casualties_hostages': casualties_hostages,
        'casualties_hostage_takers': casualties_hostage_takers,
        'hostage_takers_injured': hostage_takers_injured,
        'hostage_takers_captured': hostage_takers_captured,
        'negotiation_outcome': negotiation_outcome,
        'negotiation_duration': negotiation_duration,
        'entry_points': entry_points,
        'hostage_health_status': hostage_health_status,
        'hostage_taker_strength': hostage_taker_strength,
        'communication_reliability': communication_reliability
    })

# Analyze results
rescue_times = [result['rescue_time'] for result in results]
avg_rescue_time = np.mean(rescue_times)
success_rate = sum(result['hostages_rescued'] == num_hostages for result in results) / num_simulations
avg_hostages_rescued = np.mean([result['hostages_rescued'] for result in results])
avg_hostages_injured = np.mean([result['hostages_injured'] for result in results])
avg_casualties_hostages = np.mean([result['casualties_hostages'] for result in results])
avg_casualties_hostage_takers = np.mean([result['casualties_hostage_takers'] for result in results])
avg_hostage_takers_injured = np.mean([result['hostage_takers_injured'] for result in results])
avg_hostage_takers_captured = np.mean([result['hostage_takers_captured'] for result in results])
negotiation_success_rate = np.mean([result['negotiation_outcome'] for result in results])
avg_negotiation_duration = np.mean([result['negotiation_duration'] for result in results])
avg_entry_points = np.mean([result['entry_points'] for result in results])
avg_hostage_health_status = np.mean([result['hostage_health_status'] for result in results])
avg_hostage_taker_strength = np.mean([result['hostage_taker_strength'] for result in results])
avg_communication_reliability = np.mean([result['communication_reliability'] for result in results])

# Calculate success rate
success_threshold = 0.8 * num_hostages  # Define threshold (80% of hostages)
success_count = sum(result['hostages_rescued'] >= success_threshold for result in results)
success_rate = success_count / num_simulations

# Plot histograms
plt.figure(figsize=(18, 15))

plt.subplot(4, 4, 1)
plt.hist(rescue_times, bins=20, color='skyblue', edgecolor='black')
plt.title('Rescue Time Distribution')
plt.xlabel('Time (minutes)')
plt.ylabel('Frequency')

plt.subplot(4, 4, 2)
plt.hist([result['hostages_rescued'] for result in results], bins=np.arange(num_hostages + 2) - 0.5, color='salmon', edgecolor='black')
plt.title('Hostages Rescued Distribution')
plt.xlabel('Number of Hostages Rescued')
plt.ylabel('Frequency')
plt.xticks(range(num_hostages + 1))

plt.subplot(4, 4, 3)
plt.hist([result['hostages_injured'] for result in results], bins=np.arange(num_hostages + 2) - 0.5, color='lightcoral', edgecolor='black')
plt.title('Injured Hostages Distribution')
plt.xlabel('Number of Injured Hostages')
plt.ylabel('Frequency')
plt.xticks(range(num_hostages + 1))

plt.subplot(4, 4, 4)
plt.hist([result['casualties_hostages'] for result in results], bins=np.arange(num_hostages + 2) - 0.5, color='lightgreen', edgecolor='black')
plt.title('Hostage Casualties Distribution')
plt.xlabel('Number of Hostage Casualties')
plt.ylabel('Frequency')
plt.xticks(range(num_hostages + 1))

plt.subplot(4, 4, 5)
plt.hist([result['casualties_hostage_takers'] for result in results], bins=np.arange(num_hostage_takers + 2) - 0.5, color='orange', edgecolor='black')
plt.title('Hostage-Taker Casualties Distribution')
plt.xlabel('Number of Hostage-Taker Casualties')
plt.ylabel('Frequency')
plt.xticks(range(num_hostage_takers + 1))

plt.subplot(4, 4, 6)
plt.hist([result['hostage_takers_injured'] for result in results], bins=np.arange(num_hostage_takers + 2) - 0.5, color='red', edgecolor='black')
plt.title('Injured Hostage-Takers Distribution')
plt.xlabel('Number of Injured Hostage-Takers')
plt.ylabel('Frequency')
plt.xticks(range(num_hostage_takers + 1))

plt.subplot(4, 4, 7)
plt.hist([result['hostage_takers_captured'] for result in results], bins=np.arange(num_hostage_takers + 2) - 0.5, color='lightblue', edgecolor='black')
plt.title('Captured Hostage-Takers Distribution')
plt.xlabel('Number of Captured Hostage-Takers')
plt.ylabel('Frequency')
plt.xticks(range(num_hostage_takers + 1))

plt.subplot(4, 4, 8)
plt.hist([result['negotiation_outcome'] for result in results], bins=3, color='pink', edgecolor='black')
plt.title('Negotiation Success Rate Distribution')
plt.xlabel('Negotiation Success (1 = Success, 0 = Failure)')
plt.ylabel('Frequency')

plt.subplot(4, 4, 9)
plt.hist([result['negotiation_duration'] for result in results], bins=20, color='purple', edgecolor='black')
plt.title('Negotiation Duration Distribution')
plt.xlabel('Duration (minutes)')
plt.ylabel('Frequency')

plt.subplot(4, 4, 10)
plt.hist([result['entry_points'] for result in results], bins=np.arange(1, 2 * num_hostages + 2) - 0.5, color='yellow', edgecolor='black')
plt.title('Entry Points Distribution')
plt.xlabel('Number of Entry Points')
plt.ylabel('Frequency')

plt.subplot(4, 4, 11)
plt.hist([result['hostage_health_status'] for result in results], bins=20, color='cyan', edgecolor='black')
plt.title('Hostage Health Status Distribution')
plt.xlabel('Health Status (%)')
plt.ylabel('Frequency')

plt.subplot(4, 4, 12)
plt.hist([result['hostage_taker_strength'] for result in results], bins=20, color='gray', edgecolor='black')
plt.title('Hostage-Taker Strength Distribution')
plt.xlabel('Strength (Normalized)')
plt.ylabel('Frequency')

plt.subplot(4, 4, 13)
plt.hist([result['communication_reliability'] for result in results], bins=20, color='brown', edgecolor='black')
plt.title('Communication Reliability Distribution')
plt.xlabel('Reliability (%)')
plt.ylabel('Frequency')

plt.subplot(4, 4, 14)
plt.bar(['Success', 'Failure'], [success_rate, 1 - success_rate], color=['green', 'red'])
plt.title('Success Rate')
plt.xlabel('Outcome')
plt.ylabel('Frequency')

plt.subplot(4, 4, 15)
plt.hist([result['raid_time'] for result in results], bins=np.arange(raid_time_window_start, raid_time_window_end + 1) - 0.5, color='darkred', edgecolor='black')
plt.title('Raid Time Distribution')
plt.xlabel('Raid Time (minutes)')
plt.ylabel('Frequency')
plt.xticks(range(raid_time_window_start, raid_time_window_end + 1, 10))

plt.tight_layout()
plt.show()

# Calculate average raid time
avg_raid_time = np.mean([result['raid_time'] for result in results])

# Print summary statistics including raid time
print(f"Average time taken for the rescue operation: {avg_rescue_time:.2f} minutes")
print(f"Success rate: {success_rate:.2%}")
print(f"Average number of hostages rescued: {avg_hostages_rescued:.2f}")
print(f"Average number of injured hostages: {avg_hostages_injured:.2f}")
print(f"Average number of hostage casualties: {avg_casualties_hostages:.2f}")
print(f"Average number of hostage-taker casualties: {avg_casualties_hostage_takers:.2f}")
print(f"Average number of injured hostage-takers: {avg_hostage_takers_injured:.2f}")
print(f"Average number of captured hostage-takers: {avg_hostage_takers_captured:.2f}")
print(f"Negotiation success rate: {negotiation_success_rate:.2%}")
print(f"Average negotiation duration: {avg_negotiation_duration:.2f} minutes")
print(f"Average number of entry points: {avg_entry_points:.2f}")
print(f"Average hostage health status: {avg_hostage_health_status:.2f}%")
print(f"Average hostage-taker strength: {avg_hostage_taker_strength:.2f}")
print(f"Average communication reliability: {avg_communication_reliability:.2%}")
print(f"Average raid time: {avg_raid_time:.2f} minutes")
