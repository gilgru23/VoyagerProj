import * as React from 'react'
import { View, Text } from 'react-native'
import { NavigationContainer } from '@react-navigation/native'
import { createNativeStackNavigator } from '@react-navigation/native-stack'
import HomeScreen from './src/view/compenents/HomeScreen'
import Bluetooth from './src/view/compenents/Bluetooth'
import Signup from './src/view/compenents/signup'
import Login from './src/view/compenents/login'
import Communication from './src/view/compenents/Communication.js'
import PersonalInfo from './src/view/compenents/personalInfo'
const Stack = createNativeStackNavigator()

function App() {
  return (
    <NavigationContainer>
      <Stack.Navigator initialRouteName="PersonalInfo">
        <Stack.Screen name="Home" component={HomeScreen} />
        <Stack.Screen name="Bluetooth" component={Bluetooth} />
        <Stack.Screen name="signUp" component={Signup} />
        <Stack.Screen name="Login" component={Login} />
        <Stack.Screen name="Communication" component={Communication} />
        <Stack.Screen name="PersonalInfo" component={PersonalInfo} />
      </Stack.Navigator>
    </NavigationContainer>
  )
}

export default App
