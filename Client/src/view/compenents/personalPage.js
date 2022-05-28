import React from 'react'
import { ScrollView, TextInput, StyleSheet, Text } from 'react-native'
import { Colors, TouchableOpacity, View } from 'react-native-ui-lib'

export default function OldPersonalPage({ route, navigation }) {
  const [searchText, setSearchText] = React.useState('')
  const screens = [
    { id: 'Current Pods', title: 'Personal pods page' },
    { id: 'History', title: 'Dosing History' },
    { id: 'Schedule', title: 'Set Dosing Reminder' }
  ]
  return (
    <View>
      <TextInput
        style={{ padding: 10, marginBottom: 0, fontSize: 18 }}
        placeholder="Search for your component..."
        onChangeText={(text) => setSearchText(text)}
        value={searchText}
      />
      <ScrollView>
        <View bg-white>
          <View style={styles.container}>
            <Text text50 marginL-s5 marginV-s3 style={styles.header}>
              {`Hello ${route.params.consumer.firstName} you are connected to the dispenser:${route.params.device.name}`}
            </Text>
            {screens
              .map((screen) => {
                return (
                  <TouchableOpacity
                    activeOpacity={1}
                    bg-blue40
                    paddingH-s5
                    paddingV-s4
                    key={screen.title}
                    activeBackgroundColor={Colors.blue20}
                    style={{
                      borderBottomWidth: 1,
                      borderColor: Colors.white,
                      textAlign: 'left'
                    }}
                    onPress={() => {
                      // convert "unicorn.components.ActionBarScreen" -> "ActionBar"

                      navigation.navigate(screen.id)
                    }}
                  >
                    <Text white text70M style={styles.option}>
                      {screen.title}
                    </Text>
                  </TouchableOpacity>
                )
              })
              .filter(
                (item) =>
                  item.key.toLowerCase().indexOf(searchText.toLowerCase()) !==
                  -1
              )}
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
  option: {
    color: 'white'
  }
})
