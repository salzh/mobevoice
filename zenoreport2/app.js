/**
 * Created with JetBrains PhpStorm.
 * User: Pheonix
 * Date: 9/29/12
 * Time: 4:09 AM
 * To change this template use File | Settings | File Templates.
 */

Ext.Loader.setConfig({
    enabled:true,
    //disableCaching:true,
    paths:{
        'Zenoreport':'app'
    }
});
Ext.Ajax.on('requestexception', function (conn, response, options) {
    if (response.status === 302) {
        window.location = 'login.html';
    }
});
//Ext.Loader.setPath('Zenorerport', 'app');
Ext.require("Zenoreport.Function");
Ext.BLANK_IMAGE_URL = 'extjs/resources/themes/images/default/s.gif';
Ext.application({
    name:'Zenoreport',
    requires:[
        "Zenoreport.Function",
        'Zenoreport.Toolbar',
        'Zenoreport.SavedQueryFetch'
    ],
    models:[
        'SavedQuery',
        'Schema',
        'Schemas'
    ],
    stores:[
        'SavedQuery',
        'Schema',
        'Schemas',
        'andOr',
        'StringCondition'
    ],
    views:[
        'SavedQueries',
        'SelectTableGrid',
        'andOrCombo'
    ],
    autoCreateViewport:true,
    launch:function () {
        Ext.getCmp("showTables").fireEvent("click");
        Ext.getCmp("btnShowSavedQueries").handler();
        Zenoreport.Function.addOnce();
    }
});


/*

 Ext.onReady(function () {

 var container = Ext.create('Ext.container.Viewport', {

 });
 container.show();


 Ext.getCmp("showTables").fireEvent("click");
 Ext.getCmp("btnShowSavedQueries").handler();
 Zenoreport.Function.addOnce();


 }

 );*/
