/**
 * Created with JetBrains PhpStorm.
 * User: Pheonix
 * Date: 9/29/12
 * Time: 1:56 PM
 * To change this template use File | Settings | File Templates.
 */


Ext.define("Zenoreport.view.andOrCombo", {
    extend: 'Ext.form.field.ComboBox',
    store: 'andOr',
    alias: 'widget.andorcombo',
    displayField: 'name',
    valueField: 'value',
    queryMode: 'local',
    width: 50,
    emptyText: '&|'
});