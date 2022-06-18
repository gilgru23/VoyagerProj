import React from 'react'
import { ScrollView, TextInput, StyleSheet, Text, Image } from 'react-native'
import { Colors, TouchableOpacity, View } from 'react-native-ui-lib'
import { responseStatus } from '../../Config/constants'

export default function PersonalPage({ route, navigation }) {
  const [searchText, setSearchText] = React.useState('')
  const defaultScreens = [
    {
      id: 'Current Pods',
      title: 'Personal pods page',
      img: require('./assets/pod.png')
    },
    {
      id: 'History',
      title: 'Dosing History',
      img: require('./assets/dosing.png')
    },
    {
      id: 'Schedule',
      title: 'Set Dosing Reminder',
      img: require('./assets/dispenser.png')
    },
    {
      id: 'Scheduled Reminders',
      title: 'Watch Your Scheduled Reminders',
      img: require('./assets/clock.png')
    }
  ]

  const dispenserConnectionScreen = {
    id: 'BluetoothScreen',
    title: 'Connect the application to your dispenser',
    img: require('./assets/dispenser.png')
  }
  const screens = route.params.device
    ? defaultScreens
    : [...defaultScreens, dispenserConnectionScreen]

  const handleLogout = async () => {
    const response = await route.params.controller.logout()
    if (response.status === responseStatus.SUCCESS) {
      navigation.navigate('Home')
    }
  }

  return (
    <View>
      <TextInput
        style={{ padding: 10, marginBottom: 0, fontSize: 18 }}
        placeholder="Search for an option..."
        onChangeText={(text) => setSearchText(text)}
        value={searchText}
      />
      <ScrollView>
        <View bg-white>
          <Image source={require('./assets/voyagerLogo.png')} marginLeft={50} />
          <View style={styles.container}>
            <Text text50 marginL-s5 marginV-s3 style={styles.header}>
              {route.params.device
                ? `Hello ${route.params.consumer.firstName} you are connected to the dispenser:${route.params.device.name}`
                : `Hello ${route.params.consumer.firstName} you are in offline mode`}
            </Text>
            {screens
              .map((screen) => {
                console.log(screen.img)
                const imgPath = `./assets/${screen.img}`
                return (
                  <TouchableOpacity
                    activeOpacity={1}
                    bg-grey40
                    paddingH-s5
                    paddingV-s4
                    key={screen.title}
                    activeBackgroundColor={Colors.grey30}
                    style={{
                      borderBottomWidth: 1,
                      borderColor: Colors.white,
                      textAlign: 'left'
                    }}
                    onPress={() => {
                      // convert "unicorn.components.ActionBarScreen" -> "ActionBar"

                      navigation.navigate(screen.id, {
                        consumer: route.params.consumer,
                        device: route.params.device
                      })
                    }}
                  >
                    <View style={styles.card}>
                      <Text white text70M style={styles.option}>
                        {screen.title}
                      </Text>
                      <Image source={screen.img} style={styles.image} />
                    </View>
                  </TouchableOpacity>
                )
              })
              .filter(
                (item) =>
                  item.key.toLowerCase().indexOf(searchText.toLowerCase()) !==
                  -1
              )}
            <TouchableOpacity
              activeOpacity={1}
              bg-red20
              paddingH-s5
              paddingV-s4
              key={'logout'}
              activeBackgroundColor={Colors.red20}
              style={{
                borderBottomWidth: 1,
                borderColor: Colors.white
              }}
              onPress={async () => await handleLogout()}
            >
              <View style={styles.card}>
                <Text white text70M style={styles.option}>
                  Logout
                </Text>
              </View>
            </TouchableOpacity>
          </View>
        </View>
      </ScrollView>
    </View>
  )
}

const styles = StyleSheet.create({
  container: {
    textAlign: 'center'
  },
  header: {
    fontSize: 20,
    marginBottom: 10,
    textAlign: 'center',
    fontWeight: 'bold'
  },
  image: {
    // alignContent: 'center'
  },
  option: {
    color: 'white'
  },
  image: {
    width: 30,
    height: 40,
    marginLeft: 'auto'
  },
  card: {
    display: 'flex',
    flexDirection: 'row-reverse',
    alignItems: 'flex-start',
    alignContent: 'space-between'
  }
})
