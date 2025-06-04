/********************************************************************************
** Form generated from reading UI file 'splashscreen.ui'
**
** Created by: Qt User Interface Compiler version 6.9.0
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef UI_SPLASHSCREEN_H
#define UI_SPLASHSCREEN_H

#include <QtCore/QVariant>
#include <QtWidgets/QApplication>
#include <QtWidgets/QPushButton>
#include <QtWidgets/QWidget>

QT_BEGIN_NAMESPACE

class Ui_SplashScreen
{
public:
    QPushButton *startButton;
    QPushButton *exitButton;

    void setupUi(QWidget *SplashScreen)
    {
        if (SplashScreen->objectName().isEmpty())
            SplashScreen->setObjectName("SplashScreen");
        startButton = new QPushButton(SplashScreen);
        startButton->setObjectName("startButton");
        startButton->setGeometry(QRect(20, 360, 100, 30));
        exitButton = new QPushButton(SplashScreen);
        exitButton->setObjectName("exitButton");
        exitButton->setGeometry(QRect(570, 10, 20, 20));
        exitButton->setFlat(true);

        retranslateUi(SplashScreen);

        QMetaObject::connectSlotsByName(SplashScreen);
    } // setupUi

    void retranslateUi(QWidget *SplashScreen)
    {
        startButton->setText(QCoreApplication::translate("SplashScreen", "B\303\266l\303\274\305\237t\303\274r", nullptr));
        exitButton->setText(QCoreApplication::translate("SplashScreen", "X", nullptr));
        (void)SplashScreen;
    } // retranslateUi

};

namespace Ui {
    class SplashScreen: public Ui_SplashScreen {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_SPLASHSCREEN_H
