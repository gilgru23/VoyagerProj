import * as React from 'react';
import { View, Text } from 'react-native';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import HomeScreen from './HomeScreen';
import Bluetooth from './compenents/Bluetooth'
import Signup from './compenents/signup';
import Login from './compenents/login'
import Communication from './compenents/Communication';

const Stack = createNativeStackNavigator();

function App() {
  return (
    <NavigationContainer>
      <Stack.Navigator initialRouteName="HomeScreen">
        <Stack.Screen name="Home" component={HomeScreen}  />
        <Stack.Screen name="Bluetooth" component={Bluetooth} />
        <Stack.Screen name="signUp" component={Signup} />
        <Stack.Screen name="Login" component={Login} />
        <Stack.Screen name="Communication" component={Communication} />

      </Stack.Navigator>
    </NavigationContainer>
  );
}

export default App;