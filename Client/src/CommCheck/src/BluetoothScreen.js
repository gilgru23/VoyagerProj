import React from 'react'
import { Text, View, StyleSheet, ScrollView } from 'react-native'

import RNBluetoothClassic from 'react-native-bluetooth-classic'
import DeviceListScreen from './device-list/DeviceListScreen'
import ConnectionScreen from './connection/ConnectionScreen'
import { Consumer } from '../../model/Consumer'
import { responseStatus } from '../../Config/constants'
import { alert } from '../../view/compenents/utils'
// import DispenserDemo from '../../Communication/dispenserDemo'
export default class BluetoothScreen extends React.Component {
  constructor(props) {
    super(props)

    this.state = {
      device: undefined,
      bluetoothEnabled: true
    }
  }

  /**
   * Sets the current device to the application state.  This is super basic
   * and should be updated to allow for things like:
   * - multiple devices
   * - more advanced state management (redux)
   * - etc
   *z  n nmnmji8
   * @param device the BluetoothDevice selected or connected
   */
  selectDevice = async (device, registered) => {
    if (!device) {
      this.setState({ device })
    } else if (!registered) {
      const response =
        await this.props.route.params.controller.registerDispenser(
          device.address,
          device.name
        )
      if (response.status === responseStatus.SUCCESS) {
        this.setState({ device })
      } else {
        alert('Error', 'Can not connect to the device')
      }
    } else {
      this.setState({ device })
    }

    // this.setState({ device })
  }

  /**
   * On mount:
   *
   * - setup the connect and disconnect listeners
   * - determine if bluetooth is enabled (may be redundant with listener)
   */
  async componentDidMount() {
    console.log(
      'App::componentDidMount adding listeners: onBluetoothEnabled and onBluetoothDistabled'
    )
    console.log('App::componentDidMount alternatively could use onStateChanged')
    this.enabledSubscription = RNBluetoothClassic.onBluetoothEnabled((event) =>
      this.onStateChanged(event)
    )
    this.disabledSubscription = RNBluetoothClassic.onBluetoothDisabled(
      (event) => this.onStateChanged(event)
    )

    this.checkBluetootEnabled()
  }

  /**
   * Performs check on bluetooth being enabled.  This removes the `setState()`
   * from `componentDidMount()` and clears up lint issues.
   */
  async checkBluetootEnabled() {
    try {
      console.log('App::componentDidMount Checking bluetooth status')
      let enabled = await RNBluetoothClassic.isBluetoothEnabled()

      console.log(`App::componentDidMount Status: ${enabled}`)
      this.setState({ bluetoothEnabled: enabled })
    } catch (error) {
      console.log('App::componentDidMount Status Error: ', error)
      this.setState({ bluetoothEnabled: false })
    }
  }

  /**
   * Clear subscriptions
   */
  componentWillUnmount() {
    console.log(
      'App:componentWillUnmount removing subscriptions: enabled and distabled'
    )
    console.log(
      'App:componentWillUnmount alternatively could have used stateChanged'
    )
    this.enabledSubscription.remove()
    this.disabledSubscription.remove()
  }

  /**
   * Handle state change events.
   *
   * @param stateChangedEvent event sent from Native side during state change
   */
  onStateChanged(stateChangedEvent) {
    console.log(
      'App::onStateChanged event used for onBluetoothEnabled and onBluetoothDisabled'
    )

    this.setState({
      bluetoothEnabled: stateChangedEvent.enabled,
      device: stateChangedEvent.enabled ? this.state.device : undefined
    })
  }

  renderNo() {
    persons = [
      {
        id: '1',
        name: 'Earnest Green'
      },
      {
        id: '2',
        name: 'Winston Orn'
      }
    ]
    return (
      <View style={styles.container}>
        <ScrollView>
          <View>
            {persons.map((person) => {
              return (
                <View>
                  <Text style={styles.item}>{person.name}</Text>
                </View>
              )
            })}
          </View>
        </ScrollView>
      </View>
    )
  }

  render() {
    // const txt = this.state.device ? "Yes Device" : "No Device";
    // return <View><Text>{txt}</Text></View>
    return (
      //   <StyleProvider style={getTheme(platform)}>
      // <Root>
      <View>
        {!this.state.device ? (
          <DeviceListScreen
            bluetoothEnabled={this.state.bluetoothEnabled}
            selectDevice={this.selectDevice}
            navigation={this.props.navigation}
            controller={this.props.route.params.controller}
            consumer={
              this.props.route.params.consumer ||
              new Consumer('gil@gmail.com', 'Gil', 'Gruber', new Date())
            }
          />
        ) : (
          <ConnectionScreen
            device={this.state.device}
            selectDevice={this.selectDevice}
            onBack={() => this.setState({ device: undefined })}
            navigation={this.props.navigation}
            consumer={
              this.props.route.params.consumer ||
              new Consumer('gil@gmail.com', 'Gil', 'Gruber', new Date())
            }
            controller={this.props.route.params.controller}
          />
          // <DispenserDemo
          //   device={this.state.device}
          //   onBack={() => this.setState({ device: undefined })}
          //   navigation={this.props.navigation}
          //   consumer={
          //     this.props.route.params.consumer ||
          //     new Consumer('gil@gmail.com', 'Gil', 'Gruber', new Date())
          //   }
          // />
        )}
      </View>
      // </Root>
      //   </StyleProvider>
    )
  }
}

const styles = StyleSheet.create({
  container: {
    padding: 50,
    flex: 1
  },
  item: {
    padding: 20,
    fontSize: 15,
    marginTop: 5
  }
})
