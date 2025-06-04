#include "splashscreen.h"
#include "ui_splashscreen.h"
#include "startdialog.h"
#include <QPainterPath>
#include <QApplication>
#include <QPainter>
#include <QRegion>

SplashScreen::SplashScreen(QWidget *parent)
    : QWidget(parent)
    , ui(new Ui::SplashScreen)
{
    // 1) Çerçevesiz, şeffaf pencere
    setWindowFlags(Qt::FramelessWindowHint);
    setAttribute(Qt::WA_TranslucentBackground);

    ui->setupUi(this);

    // 2) Boyutu sabitle (PNG’ine göre uyarlayın)
    setFixedSize(600, 400);

    // 3) Buton bağlantıları
    connect(ui->startButton, &QPushButton::clicked,
            this, &SplashScreen::onStartClicked);
    connect(ui->exitButton, &QPushButton::clicked,
            this, &SplashScreen::onExitClicked);
}

SplashScreen::~SplashScreen()
{
    delete ui;
}

// ShowEvent’te oval maskeyi uygula
void SplashScreen::showEvent(QShowEvent *event)
{
    QWidget::showEvent(event);

    // Rounded rectangle mask (20px radius örneği)
    QPainterPath path;
    path.addRoundedRect(rect(), 20, 20);  // (xRadius, yRadius)
    QRegion mask = QRegion(path.toFillPolygon().toPolygon());
    setMask(mask);
}

// PaintEvent’te arka plan resmini çiz
void SplashScreen::paintEvent(QPaintEvent * /*event*/)
{
    QPainter p(this);
    p.setRenderHint(QPainter::SmoothPixmapTransform);

    QPixmap pix("C:/SplitForUs/assets/splash.png");
    // ← Bu satırı ekleyin:
    qDebug() << "Splash resmi yüklendi mi? pix.isNull() =" << pix.isNull();

    if (!pix.isNull()) {
        // Resmi pencere boyutuna ölçekleyip çiz
        p.drawPixmap(0, 0, width(), height(), pix);
    } else {
        // Eğer kaynak bulunamazsa siyah arka plan
        p.fillRect(rect(), Qt::black);
    }
}

void SplashScreen::onStartClicked()
{
    StartDialog *dlg = new StartDialog();
    dlg->show();
    close();
}

void SplashScreen::onExitClicked()
{
    qApp->quit();
}
