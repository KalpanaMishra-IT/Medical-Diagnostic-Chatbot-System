import React, { useState, useEffect } from 'react';
import { SafeAreaView, Text, FlatList, View, StyleSheet, TextInput, Button, ActivityIndicator } from 'react-native';
import axios from 'axios';

interface Activity {
  id: number;
  name: string;
  distance: number;
  moving_time: number;
}

const Activities = ({ accessToken }: { accessToken: string }) => {
  const [activities, setActivities] = useState<Activity[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchActivities = async () => {
      try {
        const response = await axios.get('https://www.strava.com/api/v3/athlete/activities', {
          headers: { Authorization: `Bearer ${accessToken}` },
        });
        setActivities(response.data);
      } catch (error) {
        console.error('Error fetching activities:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchActivities();
  }, [accessToken]);

  return (
    <View style={styles.activitiesContainer}>
      <Text style={styles.title}>Your Activities</Text>
      {loading ? (
        <ActivityIndicator size="large" color="#007bff" />
      ) : (
        <FlatList
          data={activities}
          renderItem={({ item }) => (
            <View style={styles.activityItem}>
              <Text style={styles.activityName}>{item.name}</Text>
              <Text style={styles.activityDetails}>{`Distance: ${item.distance} meters`}</Text>
              <Text style={styles.activityDetails}>{`Time: ${item.moving_time} seconds`}</Text>
            </View>
          )}
          keyExtractor={(item) => item.id.toString()}
        />
      )}
    </View>
  );
};

const App = () => {
  const accessToken = '47ca247c86807a098644e2192982d2bb6e406543';

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.userInfoSection}>
        <Text style={styles.sectionTitle}>User Information</Text>
        <TextInput style={styles.input} placeholder="Username" />
        <TextInput style={styles.input} placeholder="Email" />
        <TextInput style={styles.input} placeholder="Phone Number" />
        <TextInput style={styles.input} placeholder="Weight" />
        <TextInput style={styles.input} placeholder="Height" />
        <TextInput style={styles.input} placeholder="Sex" />
        <TextInput style={styles.input} placeholder="Date of Birth" />
        <TextInput style={styles.input} placeholder="Medical History" />
        <TextInput style={styles.input} placeholder="Days of Sickness" />
      </View>

      <Activities accessToken={accessToken} />

      <View style={styles.chatbotSection}>
        <Text style={styles.sectionTitle}>Health Chatbot</Text>
        <TextInput style={styles.input} placeholder="Ask me something..." />
        <Button title="Send" onPress={() => {}} />
      </View>

      <View style={styles.alertSection}>
        <Text style={styles.alertTitle}>ALERT!</Text>
        <Button title="Noticed" onPress={() => {}} />
        <Button title="Delay" onPress={() => {}} />
        <Button title="Contact Emergency Number" onPress={() => {}} />
      </View>
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f8f9fa',
    padding: 20,
  },
  sectionTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    marginBottom: 10,
  },
  input: {
    borderWidth: 1,
    borderColor: '#ced4da',
    borderRadius: 5,
    padding: 10,
    marginBottom: 10,
  },
  userInfoSection: {
    marginBottom: 20,
  },
  activitiesContainer: {
    flex: 1,
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    marginVertical: 20,
    textAlign: 'center',
    color: '#007bff',
  },
  activityItem: {
    backgroundColor: '#fff',
    padding: 15,
    marginVertical: 10,
    borderRadius: 10,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.25,
    shadowRadius: 3.84,
    elevation: 5,
  },
  activityName: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#343a40',
  },
  activityDetails: {
    fontSize: 14,
    color: '#6c757d',
  },
  chatbotSection: {
    marginTop: 20,
    padding: 20,
    backgroundColor: '#e9ecef',
    borderRadius: 10,
  },
  alertSection: {
    marginTop: 20,
    padding: 20,
    backgroundColor: '#e9ecef',
    borderRadius: 10,
    alignItems: 'center',
  },
  alertTitle: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#dc3545',
    marginBottom: 10,
  },
});

export default App;
