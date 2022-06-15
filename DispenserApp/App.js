import * as React from 'react'
import { NavigationContainer } from '@react-navigation/native'
import { createNativeStackNavigator } from '@react-navigation/native-stack'
import { Controller } from './src/controller/controller'
import BluetoothScreen from './src/CommCheck/src/BluetoothScreen'

const Stack = createNativeStackNavigator()

function App() {
  const controller = new Controller()
  return (
    <NavigationContainer>
      <Stack.Navigator initialRouteName="Dispenser Demo">
        <Stack.Screen
          name="Dispenser Demo"
          component={BluetoothScreen}
          initialParams={{ controller: controller }}
        />
      </Stack.Navigator>
    </NavigationContainer>
  )
}

export default App
