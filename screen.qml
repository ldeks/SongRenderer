import QtQuick 2.7
import QtGraphicalEffects 1.0

Rectangle {
    id: screen
    width: 1000
    height: 600

    function setFont(font) {
        songText.font = font
    }

    function getFont() {
        return songText.font
    }

    function setTextOpacity(value) {
        if (value <= 1.0 && value >= 0.0)
            songText.opacity = value
        setTextBlur(false)
        setDropShadow(false)
    }

    function setTextBlur(blurEnabled) {
        blurText.visible = blurEnabled
        dropShadow.visible = false
        songText.visible = !(blurText.visible || dropShadow.visible)
    }

    function setDropShadow(dropShadowEnabled) {
        dropShadow.visible = dropShadowEnabled
        blurText.visible = false
        songText.visible = !(blurText.visible || dropShadow.visible)
    }

    Image {
        source: "geo5.jpg"
        anchors.fill: parent
    }

    Text {
        id: songText
        text: "Praise to the Lord\nthe Almighty\nThe King of Creation"
        anchors.centerIn: parent
        font.family: "The Girl Next Door"
        font.pointSize: 48
        color: "white"
        visible: true
    }

    FastBlur {
        id: blurText
        anchors.fill: songText
        radius: 47
        transparentBorder: true
        source: songText
        visible: false
    }

    DropShadow {
        id: dropShadow
        anchors.fill: songText
        horizontalOffset: 3
        radius: 8.0
        samples: 17
        //color: "#80000000"
        color: "gray"
        source: songText
        visible: false
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
