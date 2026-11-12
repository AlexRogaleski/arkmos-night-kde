/*
    Tela de abertura do Arkmos Night: o nome sobre o fundo do Tokyo Night e uma
    barra que avança a cada etapa do login.

    SPDX-License-Identifier: MIT
*/

import QtQuick
import org.kde.kirigami as Kirigami

Rectangle {
    id: root
    color: "#1a1b26"

    // O KSplash avança de 1 a 5 enquanto a sessão sobe.
    property int stage
    readonly property int lastStage: 5

    onStageChanged: {
        if (stage == 2) {
            introAnimation.running = true;
        }
    }

    Item {
        id: content
        anchors.fill: parent
        opacity: 0

        Column {
            anchors.centerIn: parent
            spacing: Kirigami.Units.gridUnit * 1.5

            Text {
                anchors.horizontalCenter: parent.horizontalCenter
                text: "Arkmos Night"
                color: "#c0caf5"
                font.pointSize: 30
                font.weight: Font.Light
                font.letterSpacing: 2
            }

            Rectangle {
                id: track
                anchors.horizontalCenter: parent.horizontalCenter
                width: Kirigami.Units.gridUnit * 14
                height: 4
                radius: 2
                color: "#292e42"

                Rectangle {
                    height: parent.height
                    radius: parent.radius
                    color: "#7aa2f7"
                    width: track.width * Math.max(0, Math.min(root.stage, root.lastStage)) / root.lastStage

                    Behavior on width {
                        NumberAnimation {
                            duration: Kirigami.Units.longDuration * 2
                            easing.type: Easing.InOutQuad
                        }
                    }
                }
            }
        }
    }

    OpacityAnimator {
        id: introAnimation
        running: false
        target: content
        from: 0
        to: 1
        duration: Kirigami.Units.veryLongDuration * 2
        easing.type: Easing.InOutQuad
    }
}
