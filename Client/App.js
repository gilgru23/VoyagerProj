import * as React from 'react'
import { View, Text } from 'react-native'
import { NavigationContainer } from '@react-navigation/native'
import { createNativeStackNavigator } from '@react-navigation/native-stack'
import HomeScreen from './src/view/compenents/HomeScreen'
import Signup from './src/view/compenents/signup'
import Login from './src/view/compenents/login'
import Communication from './src/view/compenents/Communication.js'
import PersonalInfo from './src/view/compenents/personalInfo'
import PersonalPods from './src/view/compenents/personalPods'
import CurrPod from './src/view/compenents/currPod'
import Schedule from './src/view/compenents/Schedule'
import { MockServer } from './src/Communication/mockServer'
import { Controller } from './src/controller/controller'
import BluetoothScreen from './src/CommCheck/src/BluetoothScreen'
import ConnectionScreen from './src/CommCheck/src/connection/ConnectionScreen'
import History from './src/view/compenents/history'
import PersonalPage from './src/view/compenents/personalPage'
import DosingFeeback from './src/view/compenents/dosingFeedback'
import ScheduledReminders from './src/view/compenents/scheduledReminders'

const Stack = createNativeStackNavigator()

function App() {
  const controller = new Controller()
  return (
    <NavigationContainer>
      <Stack.Navigator initialRouteName="Home">
        <Stack.Screen name="Home" component={HomeScreen} />
        <Stack.Screen
          name="Dosing Feedback"
          component={DosingFeeback}
          initialParams={{ controller: controller }}
        />
        <Stack.Screen
          name="Personal Page"
          component={PersonalPage}
          initialParams={{ controller: controller }}
        />
        <Stack.Screen
          name="History"
          component={History}
          initialParams={{ controller: controller }}
        />
        <Stack.Screen
          name="Connection"
          component={ConnectionScreen}
          initialParams={{ controller: controller }}
        />
        <Stack.Screen
          name="RegisterPod"
          component={ConnectionScreen}
          initialParams={{ controller: controller }}
        />
        <Stack.Screen
          name="BluetoothScreen"
          component={BluetoothScreen}
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
          name="Current Pods"
          component={CurrPod}
          initialParams={{ controller: controller }}
        />
        <Stack.Screen
          name="Schedule"
          component={Schedule}
          initialParams={{ controller: controller }}
        />
        <Stack.Screen
          name="Scheduled Reminders"
          component={ScheduledReminders}
          initialParams={{ controller: controller }}
        />
      </Stack.Navigator>
    </NavigationContainer>
  )
}

export default App
