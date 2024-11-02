from behave import *
from app import App
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QLineEdit, QMessageBox
from PyQt6.QtCore import Qt
from database_module import add_record, get_data, update_record, delete_record

@given('я открыл приложение')
def step_impl(context):
    app = QApplication([])
    context.app = App()
    context.app.show()
    app.processEvents()

@when('я ввожу "{text}" в поле "{field}"')
def step_impl(context, text, field):
    context.app.findChild(QLineEdit, field).setText(text)
    context.app.processEvents()



@then('запись с названием "{name}" и ценой "{price}" должна быть добавлена в базу данных')
def step_impl(context, name, price):
    assert context.app.is_record_in_database(name, price)

@then('должно появиться сообщение об ошибке')
def step_impl(context):
    assert context.app.error_message_is_visible()

@when('я перехожу на вкладку "{tab}"')
def step_impl(context, tab):
    context.app.findChild(QWidget, tab).click()
    context.app.processEvents()

@then('должны отображаться все записи из базы данных')
def step_impl(context):
    assert context.app.all_records_are_visible()

@then('должны отображаться только записи с названием "{name}"')
def step_impl(context, name):
    assert context.app.records_with_name_are_visible(name)

@when('я выбираю запись с названием "{name}"')
def step_impl(context, name):
    context.app.select_record_by_name(name)
    context.app.processEvents()

@then('запись с названием "{name}" и ценой "{price}" должна быть обновлена в базе данных')
def step_impl(context, name, price):
    assert context.app.is_record_updated_in_database(name, price)

@then('запись с названием "{name}" должна быть удалена из базы данных')
def step_impl(context, name):
    assert not context.app.is_record_in_database(name)

@when('я нажимаю кнопку "Открыть окно"')
def step_impl(context):
    context.app.find_child(QPushButton, "Открыть окно").click()
    context.app.processEvents()

@then('должно открыться новое окно')
def step_impl(context):
    assert context.app.new_window_is_visible()

@then('должны отображаться данные из базы данных')
def step_impl(context):
    assert context.app.database_data_is_visible()