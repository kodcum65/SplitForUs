#ifndef SPLASHSCREEN_H
#define SPLASHSCREEN_H

#include <QWidget>
#include <QShowEvent>
#include <QPaintEvent>

namespace Ui {
class SplashScreen;
}

class SplashScreen : public QWidget
{
    Q_OBJECT

public:
    explicit SplashScreen(QWidget *parent = nullptr);
    ~SplashScreen();

protected:
    void showEvent(QShowEvent *event) override;   // oval maske
    void paintEvent(QPaintEvent *event) override; // resmi çiz

private slots:
    void onStartClicked();
    void onExitClicked();

private:
    Ui::SplashScreen *ui;
};

#endif // SPLASHSCREEN_H
