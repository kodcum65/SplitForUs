#include <QApplication>
#include "splashscreen.h"

int main(int argc, char *argv[])
{
    QApplication app(argc, argv);
     app.setWindowIcon(QIcon("C:/SplitForUs/assets/app_icon.ico"));
    SplashScreen splash;
    splash.show();

    return app.exec();
}
