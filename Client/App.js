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
import PersonalPage from './src/view/compenents/personalPage'
import PersonalPods from './src/view/compenents/personalPods'
import CurrPod from './src/view/compenents/currPod'
import Schedule from './src/view/compenents/Schedule'
import { MockServer } from './src/Communication/mockServer'
import { Controller } from './src/controller/controller'
import BluetoothScreen from './src/CommCheck/src/BluetoothScreen'
import ConnectionScreen from './src/CommCheck/src/connection/ConnectionScreen'

const Stack = createNativeStackNavigator()

function App() {
  const controller = new Controller()
  return (
    <NavigationContainer>
      <Stack.Navigator initialRouteName="Home">
        <Stack.Screen name="Home" component={HomeScreen} />
        <Stack.Screen
          name="Connection"
          component={ConnectionScreen}
          initialParams={{ controller: controller }}
        />
        <Stack.Screen
          name="BluetoothScreen"
          component={BluetoothScreen}
          initialParams={{ controller: controller }}
        />
        <Stack.Screen
          name="Bluetooth"
          component={Bluetooth}
          initialParams={{ controller: controller }}
        />
        <Stack.Screen
          name="signUp"
          component={Signup}
          initialParams={{ controller: controller }}
        />
        <Stack.Screen
          name="Login"
          component={Login}
          initialParams={{ controller: controller }}
        />
        <Stack.Screen
          name="Communication"
          component={Communication}
          initialParams={{ controller: controller }}
        />
        <Stack.Screen
          name="PersonalInfo"
          component={PersonalInfo}
          initialParams={{ controller: controller }}
        />
        <Stack.Screen
          name="PersonalPage"
          component={PersonalPage}
          initialParams={{ controller: controller }}
        />
        <Stack.Screen
          name="PersonalPods"
          component={PersonalPods}
          initialParams={{ controller: controller }}
        />
        <Stack.Screen
          name="Current Pod"
          component={CurrPod}
          initialParams={{ controller: controller }}
        />
        <Stack.Screen
          name="Scheduler"
          component={Schedule}
          initialParams={{ controller: controller }}
        />
      </Stack.Navigator>
    </NavigationContainer>
  )
}

export default App
