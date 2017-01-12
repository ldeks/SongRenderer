import QtQuick 2.7

Rectangle {
    id: screen
    width: 1000
    height: 600

    Image {
        source: "geo5.jpg"
        anchors.fill: parent
    }

    Text {
        text: "Praise to the Lord\nthe Almighty\nThe King of Creation"
        anchors.centerIn: parent
        font.family: "The Girl Next Door"
        font.pointSize: 48
        color: "white"
    }

    Text {
        text: "Author: Joachim Neander\nCopyright: Public Domain"
        anchors.left: parent.left
        anchors.bottom: parent.bottom
        font.family: "PT Sans"
        font.pointSize: 11
        color: "white"
    }
}
