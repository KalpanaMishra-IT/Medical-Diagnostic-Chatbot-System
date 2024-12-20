import React, { useState } from 'react';
import { SafeAreaView, Button, View } from 'react-native';
import Activities from './Activities';

const App = () => {
  const accessToken = '47ca247c86807a098644e2192982d2bb6e406543';

  return (
    <SafeAreaView style={{ flex: 1 }}>
      <View style={{ padding: 20 }}>
        <Activities accessToken={accessToken} />
      </View>
    </SafeAreaView>
  );
};

export default App;
