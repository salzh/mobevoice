/**
 * Created with JetBrains PhpStorm.
 * User: Pheonix
 * Date: 9/29/12
 * Time: 5:45 AM
 * To change this template use File | Settings | File Templates.
 */


Ext.define('Zenoreport.store.SavedQuery', {
    extend:'Ext.data.Store',
    requires:[
        'Zenoreport.model.SavedQuery'
    ],
    autoLoad:true,
    constructor:function (cfg) {
        var me = this;
        cfg = cfg || {};
        me.callParent([Ext.apply({
            storeId:'SavedQuery',
            model:'Zenoreport.model.SavedQuery',
            proxy:{
                type:'ajax',
                url:'database.php?action=getSaved',
                reader:{
                    type:'json',
                    root:'queries'
                }
            }
        }, cfg)]);
    }
});