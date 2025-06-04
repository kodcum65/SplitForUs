#ifndef STARTDIALOG_H
#define STARTDIALOG_H

#include <QDialog>
#include <QWidget>   // veya <QDialog> / <QMainWindow>
#include <QMainWindow>
#include "ui_StartDialog.h"

namespace Ui {
class StartDialog;
}

class StartDialog : public QDialog
{
    Q_OBJECT

public:
    explicit StartDialog(QWidget *parent = nullptr);
    ~StartDialog();

private:
    Ui::StartDialog *ui;
};

#endif // STARTDIALOG_H
