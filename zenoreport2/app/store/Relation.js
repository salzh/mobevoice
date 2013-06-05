/**
 * Created with JetBrains PhpStorm.
 * User: Pheonix
 * Date: 9/29/12
 * Time: 2:31 PM
 * To change this template use File | Settings | File Templates.
 */


Ext.define("Zenoreport.store.Relation", {
    extend:'Ext.data.Store',
    requires: [
        'Zenoreport.model.Relation'
    ],
    constructor:function (cfg) {
        cfg = cfg || {};
        this.callParent([Ext.apply({
            storeId:'Relation',
            model:'Zenoreport.model.Relation',
            data:relations
        }, cfg)])

    }
});