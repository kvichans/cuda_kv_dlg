import unittest

import os, tempfile, itertools
from cudatext       import *
from cuda_kv_base   import *
from cuda_kv_dlg    import *

pass;                           _ONLY = []              # Only names from the list
pass;                          #_ONLY = ['ag_1']
pass;                          #_ONLY = ['ag_pos']
pass;                          #_ONLY = ['ag_cattr']
pass;                          #_ONLY = ['ag_cols']
pass;                          #_ONLY = ['ag_anchor']
pass;                           _ONLY = ['ag_meta']
pass;                          #_ONLY = ['ag_menu']
pass;                          #_ONLY = ['ag_repro']
pass;                          #_ONLY = ['ag_dict']
pass;                          #_ONLY = ['ag_border']
pass;                          #_ONLY = ['ag_dock']
pass;                          #_ONLY = ['ag_onetime_nonmodal']
pass;                          #_ONLY = ['ag_reset']
pass;                          #_ONLY = ['ag_tid']

def powerset(iterable):
    """ 10.1.2. Itertools Recipes
        powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)
    """
    s = list(iterable)
    return itertools.chain.from_iterable(itertools.combinations(s, r) for r in range(len(s)+1))

class AnyClass: # From t.me/pythonetc at 01feb19
    def __eq__(self, another):
        return True
ANY = AnyClass()

class TestDlgAg(unittest.TestCase):


    ##############################
    def test_ag_1(self):
        # Controls: label, edit, button
        # Tricks: tid, >, def_bt, call, update, hide, on_exit, cattr, cval, fid
        test_str    = 'test_ag_1'
        if                      _ONLY and test_str[5:] not in _ONLY: return
        val4edit    = 'Edit me'
        pass;                  #log('val4edit={}',(val4edit))
        def do_acts(ag, name, data=''):
            log('on call {}',name)
            if name=='b1':
                return    dict(ctrls=[('b1', dict(cap='Renamed'))]  # New cap
                              ,fid='b2')    # Next focus
            if name=='b2':
                x = ag.cattr('b2', 'x')
                w = ag.cattr('b2', 'w')
                ag.update(dict(ctrls=[('b2', dict(x=x+20, w=w-40))] # New position
                              ,fid='b3'))   # Next focus
                return []   # No changes
            if name=='b3':
                app.msg_box('Ask something', app.MB_OKCANCEL)
#               ag.hide('b3')
                return None # Close dlg
            return []
        def do_exit(ag):
            nonlocal val4edit
            val4edit = ag.val('e1')
        ag  = DlgAg(
            ctrls=[0
    ,('b1',dict(tp='bttn',cap='Re&name me' ,x= 0 ,y=  0    ,w=200  ,on=do_acts))
    ,('l1',dict(tp='labl',cap='>he&re'     ,x= 0 ,tid='e1' ,w= 50))
    ,('e1',dict(tp='edit',val=val4edit     ,x=50 ,y= 30    ,w=150))
    ,('b2',dict(tp='bttn',cap='Sh&ort me'  ,x= 0 ,y= 60    ,w=200  ,on=do_acts))
    ,('b3',dict(tp='bttn',cap='A&sk,Close' ,x= 0 ,y= 90    ,w=200  ,on=do_acts))
    ,('cl',dict(tp='bttn',cap='Close'      ,x= 0 ,y=120    ,w=200  ,on=CB_HIDE   ,def_bt=1))
                  ][1:]
        ,   form=dict(cap=test_str               ,h=150    ,w=200)
        ,   fid='e1'    # Start focus
        )
        (rt,vs) = ag.show(do_exit)
        pass;                   log('rt,vs={}',(rt,vs))
        pass;                  #log('val4edit={}',(val4edit))
        self.assertTrue(True)


    ##############################
    def test_ag_cattr(self):
        test_str= 'test_ag_cattr'
        if                      _ONLY and test_str[5:] not in _ONLY: return
        mv  = ['memo\ttext', 'line2']
        def do_acts(ag, name, data=''):
            ca  = ag.cattr
            cas = ag.cattrs
            leq = self.assertListEqual
            with self.assertRaises(ValueError):
                ca('nono', 'x')
            if name=='b1':
#               printf('labl l.tp={} l.type={} m.tp={} m.type={}',ca('l1', 'tp'),ca('l1', 'type'),ca('l1', 'tp', live=False),ca('l1', 'type', live=False))
                leq([ca('l1', 'tp') ,ca('l1', 'type') ,ca('l1', 'tp', live=False) ,ca('l1', 'type', live=0) ]
                   ,['labl'            ,'label'             ,'labl'                        ,'label'         ])
                printf('labl all={}',cas('l1'))
#               printf('labl[au] {}',cas('l1', ['au']))
#               printf('labl[au,x] {}',cas('l1', ['au','x']))
#               printf('labl au={} autosize={}',ca('l1', 'au'),ca('l1', 'autosize'))
                leq([cas('l1', ['au']), cas('l1', ['au','x']), ca('l1', 'au'), ca('l1', 'autosize') ]
                   ,[{'au': True}        , {'au': True, 'x': ANY}  , True             , True        ])
#               printf('labl l.x={} m.x={}',ca('l1', 'x'),ca('l1', 'x', live=0))
#               printf('labl l.w={} m.w={}',ca('l1', 'w'),ca('l1', 'w', live=0))
#               printf('labl l.r={} m.r={}',ca('l1', 'r'),ca('l1', 'r', live=0))
                leq([ca('l1', 'x'),ca('l1', 'x', live=0),ca('l1', 'w'),ca('l1', 'w', live=0),ca('l1', 'r'),ca('l1', 'r', live=0)]
                   ,[ANY          ,None                 ,ANY          ,100                  ,ANY          ,None                 ])

                printf('l.cols={}',ca('v1', 'cols'))
                printf('m.cols={}',ca('v1', 'cols', live=0))
#               printf('l.cols_ws={}',ca('v1', 'cols_ws'))
#               printf('m.cols_ws={}',ca('v1', 'cols_ws', live=0))
                leq([ca('v1', 'cols_ws'), ca('v1', 'cols_ws', live=0)]
                   ,[[ANY,ANY,ANY]      , None                       ])
#               printf('l.[x,cols_ws]={}',cas('v1', ['x', 'cols_ws']))
#               printf('m.[x,cols_ws]={}',cas('v1', ['x', 'cols_ws'], live=0))
                leq([cas('v1', ['x', 'cols_ws'])        , cas('v1', ['x', 'cols_ws'], live=0)   ]
                   ,[{'x':10, 'cols_ws':[ANY,ANY,ANY]}  , {'x':10, 'cols_ws':None}              ])
#               printf('l.[a,cols_ws]={}',cas('v1', ['a', 'cols_ws']))
#               printf('m.[a,cols_ws]={}',cas('v1', ['a', 'cols_ws'], live=0))
                leq([cas('v1', ['a', 'cols_ws'])        , cas('v1', ['a', 'cols_ws'], live=0)   ]
                   ,[{'a':'r>', 'cols_ws':[ANY,ANY,ANY]}, {'a':'r>', 'cols_ws':None}            ])
                
#               printf('l.fid={} m.fid={}',ag.focused(),ag.focused(0))
                leq([ag.focused(),ag.focused(0) ]
                   ,['b1'        ,'b1'          ])

#               printf('m l.val={} m.val={}',ca('m1', 'val'),ca('m1', 'val', live=0))
#               printf('m l.val={}',ag.val('m1'))
#               printf('l.vals={} m.vals={}',    ag.vals(),    ag.vals(0))
                leq([ca('m1', 'val'), ca('m1', 'val', live=0), ag.val('m1'), ag.val('m1',0) ]
                   ,[mv             ,mv                      , mv          , mv             ])
                leq([ag.vals()          , ag.vals(0)        ]
                   ,[{'m1':mv, 'v1':1}  , {'m1':mv, 'v1':1} ])
            if name=='bttn2':
                w   = ag.fattr('w')
                return  {'form':{'w':w+100}}
            return []
        def on_resize(ag,k,d):
            pass;#print('on_resize '+test_str)
        its = ([('h1',60),('h2',70),('h3',30)], [['a_1','a_2','a_3'],['b_1','b_2','b_3'],['c_1','c_2','c_3']])
#       cls = [{'hd':'h1', 'al':'C', 'au':False}
#             ,{'hd':'h2', 'al':'R', 'au':False, 'mi':40}
#             ,{'hd':'h3', 'al':'R', 'au':True }
#             ]
#       ws  = [60, 70, 30]
        DlgAg(
            ctrls=[0
    ,('b1',dict(tp='bttn',cap='Click me to test attrs'    
                                            ,x=10   ,w=100  ,y=  5              ,a='--' ,au=True   ,def_bt=True    ,on=do_acts))
    ,('l1',dict(tp='labl',cap='autosized text'       ,w=100  ,y= 30              ,a='--' ,au=True))
    ,('m1',dict(tp='memo'                    ,x=10   ,w=180  ,y= 60      ,h=60   ,a='r>'         ))
    ,('v1',dict(tp='livw',items=its          ,x=10   ,w=180  ,y=130      ,h=80   ,a='r>' ,grid=True  ))
    ,('b2',dict(tp='bttn',cap='Resize form'  ,x=10   ,w=100  ,y=225              ,a='--'                            ,on=do_acts))
                  ][1:]
        ,   form=odct(cap=test_str                   ,w=200              ,h=300      
                     ,on_resize=on_resize
                     )
        ,   vals=dict(
                      m1=mv,
                      v1=1,
                     )
        ,   fid='b1'
        ).show()
#       ).gen_repro_code('test_repro_cattr.py').show()
        self.assertTrue(True)


    ##############################
    def test_ag_cols(self):
        test_str= 'test_ag_cols'
        if                      _ONLY and test_str[5:] not in _ONLY: return
        def do_acts(ag, name, data=''):
            ca  = ag.cattr
            cas = ag.cattrs
            if name=='bttn1':
#               printf('livw l.cols={}',ca('livw1', 'cols'))
#               printf('livw m.cols={}',ca('livw1', 'cols', live=False))
                printf('livw l.cols_ws={}',ca('livw1', 'cols_ws'))
                printf('livw m.cols_ws={}',ca('livw1', 'cols_ws', live=False))
#               printf('livw l.cols_ws={}',cas('livw1', ['x', 'cols_ws']))
#               printf('livw m.cols_ws={}',cas('livw1', ['x', 'cols_ws'], live=False))
#               printf('livw l.cols_ws={}',cas('livw1', ['a', 'cols_ws']))
#               printf('livw m.cols_ws={}',cas('livw1', ['a', 'cols_ws'], live=False))
#               printf('memo l.val={}',ag.val('memo1'))
                printf('l.vals={}',    ag.vals())
            if name=='bttn2':
                return  {'form':{'w':ag.fattr('w')+100}}
            return []
        def on_resize(ag,k,d):
            pass;#print('on_resize '+test_str)
        its = ([('h1',60),('h2',70),('h3',30)], [['a_1','a_2','a_3'],['b_1','b_2','b_3'],['c_1','c_2','c_3']])
        cls = [{'hd':'h1', 'al':'C', 'au':False}
              ,{'hd':'h2', 'al':'L', 'au':False, 'mi':40}
              ,{'hd':'h3', 'al':'R', 'au':True }
              ]
        ws  = [60, 70, 30]
        DlgAg(
            ctrls=[0
    ,('bttn1',dict(tp='bttn',cap='Get attrs'    ,x=10   ,w=100  ,y=  5              ,a='--' ,def_bt=True    ,on=do_acts))
    ,('bttn2',dict(tp='bttn',cap='Resize form'  ,x=10   ,w=100  ,y= 35              ,a='--'                 ,on=do_acts))
    ,('livw1',dict(tp='livw',items=its
#                           ,cols=cls 
#                           ,columns=cls 
#                           ,cols_ws=ws         
                                                ,x=10   ,w=180  ,y= 70      ,h=80   ,a='r>' ,grid=True  ))
                  ][1:]
        ,   form=odct(cap=test_str                      ,w=200              ,h=200      
                     ,on_resize=on_resize
                     )
        ,   vals=dict(
                      livw1=1,
                     )
        ,   fid='bttn1'
        ,   opts=dict(foo=0
                     ,store_col_widths=['livw1']
                     ,auto_stretch_col={'livw1':1}
                     ,auto_start_col_width_on_min=['livw1']
                     )
        ).show()
#       ).gen_repro_code('test_repro_cols.py').show()
        self.assertTrue(True)


    ##############################
    def test_ag_pos(self):
        test_str= 'test_ag_pos'
        if                      _ONLY and test_str[5:] not in _ONLY: return
        DlgAg(
            ctrls=[0
    ,('labl1',dict(tp='labl',cap='labl h=30'    ,x=  0  ,w=100  ,y=  0      ,h=30   ,border=True))
    ,('bttn1',dict(tp='bttn',cap='bttn h=30'    ,x=110  ,w=100  ,y=  0      ,h=30   ))
    ,('chbt1',dict(tp='chbt',cap='chbt h=30'    ,x=220  ,w=100  ,y=  0      ,h=30   ))
    ,('edit1',dict(tp='edit',val='edit h=30'    ,x=330  ,w=100  ,y=  0      ,h=30   ))
    ,('cmbx1',dict(tp='cmbx',val='cmbx h=30'    ,x=440  ,w=100  ,y=  0      ,h=30   ))
    ,('cmbr1',dict(tp='cmbr',val=0              ,x=550  ,w=100  ,y=  0      ,h=30   ,items=['cmbr h=30']))
    ,('sped1',dict(tp='sped',cap='sped h=30'    ,x=  0  ,w=100  ,y= 50      ,h=30   ))
    ,('chck1',dict(tp='chck',cap='chck h=30'    ,x=110  ,w=100  ,y= 50      ,h=30   ,border=True))
    ,('rdio1',dict(tp='rdio',cap='rdio h=30'    ,x=220  ,w=100  ,y= 50      ,h=30   ,border=True))
    ,('lilb1',dict(tp='lilb',cap='lilb h=30'    ,x=330  ,w=100  ,y= 50      ,h=30   ,border=True))
                  ][1:]
        ,   form=dict(cap=test_str                      ,w=660              ,h=160      
                     ,frame='resize')
        ,   fid='edit1'    # Start focus
        ).show()
        self.assertTrue(True)


    ##############################
    def test_ag_anchor(self):
        test_str= 'test_ag_anchor'
        if                      _ONLY and test_str[5:] not in _ONLY: return
        def on_resize(ag,k,d):
            print('on_resize '+test_str)
#           return []
        DlgAg(
            ctrls=[0
    ,('b1',dict(tp='bttn',cap='def'     ,x=  0  ,w=100  ,y=  0              ))
#   ,('l1',dict(tp='labl',cap='>def'    ,x=110  ,w= 40  ,tid='e1'           ))
#   ,('e1',dict(tp='edit',val='r>'      ,x=150  ,w= 50  ,y=  0              ,a='r>'))
#   ,('b3',dict(tp='bttn',cap='--'     ,_x=  0 ,_w=100  ,y= 30              ,a='--'     ,au=True))
#   ,('m1',dict(tp='memo',val='r>b.'    ,x=  0  ,w=100  ,y= 60      ,h=60   ,a='r>b.'   ,ro_mono_brd='1,0,1'))
#   ,('m2',dict(tp='memo',cap='>>||'    ,x=110  ,w= 90              ,h=50   ,a='>>||'   ,ro_mono_brd='1,1,0'))
#   ,('cl',dict(tp='bttn',cap='>>..'    ,x= 90  ,w=110  ,y=130              ,a='>>..'))
                  ][1:]
        ,   form=dict(cap=test_str              ,w=200  ,h=160
                     ,on_resize=on_resize
#                    ,frame='resize'
                     )
#       ,   fid='e1'    # Start focus
#       ).gen_repro_code('test_repro_anchor.py').show()
        ).show()
        self.assertTrue(True)


    ##############################
    def test_ag_meta(self):
        test_str= 'test_ag_meta'
        if                      _ONLY and test_str[5:] not in _ONLY: return
        def act_on_cY():
            app.msg_box('Done "Cmd with Ctrl|Meta hotkey"', app.MB_OK)
            print('act_on_cY - OK')
            return []
        def wnen_menu(ag, tag):
            if tag=='cY':   return act_on_cY()
        def do_menu(ag, name, data=''):
            mn_its = [0
                    ,dict(cap='&Cmd with Ctrl|Meta hotkey' ,tag='cY'   ,key='Ctrl+Y')
                    ][1:]
            return ag.show_menu(mn_its, name, cmd4all=wnen_menu)
           #def do_menu
        l1_h    =('...Ctrl+Y...'
                '\r...Ctrl+Shift+Y...'
                '\r...Alt+Ctrl+Y...'
                 )
        def acts(ag, name, data=''):
            scam= ag.scam()
            if 'c' in scam:
                app.msg_box('Done Ctrl|Meta+Click', app.MB_OK)
            return []
        DlgAg(
            ctrls=[0
    ,('b1',dict(tp='bttn',cap='Show menu &='        ,au=True    ,y= 10  ,a='--' ,on=do_menu,on_menu=do_menu))
    ,('l1',dict(tp='labl',cap='Hint with Ctrl|Meta' ,au=True    ,y= 43  ,a='--' ,hint=l1_h  ))
    ,('b2',dict(tp='bttn',cap='Wait Ctrl|Meta+Click',au=True    ,y= 70  ,a='--' ,on=acts))
                  ][1:]
        ,   form=dict(cap=test_str                          ,w=200  ,h=160)
#       ,   opts={'ctrl_to_meta':'need'}
        ,   opts={'ctrl_to_meta':'by_os'}
        ).show()
#       ).gen_repro_code('test_repro_anchor.py').show()
        self.assertTrue(True)


    ##############################
    def test_ag_menu(self):
        test_str= 'test_ag_menu'
        if                      _ONLY and test_str[5:] not in _ONLY: return
        chk     = True
        act_rd  = 'mr2'
        def wnen_menu(ag, tag):
            nonlocal chk, act_rd
            chk     = not chk   if tag in ('mc1','mc3')         else chk
            act_rd  = tag       if tag in ('mr1','mr2','mr3')   else act_rd
            print('wnen_menu: tag=',tag)
            return None if tag=='m1' else []
        def do_menu(ag, name, data=''):
            mn_its = [0
    ,dict(cap='Clos&e dialog'   , tag='m1'                          ,key='Esc')
    ,dict(cap='&Cmd un'         , tag='m2'              , en=False  ,key='Ctrl+Enter')
    ,dict(cap='-')
    ,dict(cap='Check/&mark'     , tag='mc1' , mark=('c' if chk else ''))           
    ,dict(cap='Check/mark un'   , tag='mc2' , mark='c'  , en=False  ,key='Ctrl++')
    ,dict(cap='Check/&ch'       , tag='mc3' , ch=chk)           
    ,dict(cap='Check/ch un'     , tag='mc4' , ch=True   , en=False  ,key='Ctrl+Shift+C')
    ,dict(cap='-')
    ,dict(cap='Radio group'                             , en=False)
    ,dict(cap='mr&1: Select me' , tag='mr1' , mark=('r' if act_rd=='mr1' else ''))
    ,dict(cap='mr&2: Select me' , tag='mr2' , rd=(act_rd=='mr2'))
    ,dict(cap='mr&3: Select me' , tag='mr3'             , en=False)
    ,dict(cap='-')
    ,dict(cap='&Sub', sub=
        [0
    ,dict(cap='Sub &1'          , tag='s1'  )
    ,dict(cap='-')
    ,dict(cap='Sub &2'          , tag='s2'  )
        ][1:])
                    ][1:]
#           set_all_for_tree(mn_its, 'sub', 'cmd', wnen_menu)       # All nodes have cmd
            where, dx, dy   =(('dxdy', 7+data['x'], 7+data['y'])    # To show near cursor
                                if type(data)==dict else \
                              ('+h', 0, 0)                          # To show under control
                             )
            return ag.show_menu(mn_its
                , name, where, dx, dy
                , cmd4all=wnen_menu                                 # All nodes have same handler
                , repro_to_file='test_ag_menu.py' if where=='dxdy' else ''
            )
        DlgAg(
            ctrls=[0
                ,('b1',dict(tp='bttn'  ,x=0,y=  0   ,w=200          ,cap='RightClick me'
                    ,on_menu=CBP_WODATA(do_menu)))
                ,('m1',dict(tp='memo'  ,x=0,y= 30   ,w=200   ,h=100 ,val='RightClick \nanywhere \ninside me'
                    ,on_mouse_down=lambda ag, name, data='':
                        do_menu(ag, name, data) if 1==data['btn'] else []))
                  ][1:]
        ,   form=dict(cap=test_str                  ,w=200  ,h=130)
        ,   fid='b1'    # Start focus
        ).show()
        self.assertTrue(True)


    ##############################
    def test_ag_repro(self):
        test_str= 'test_ag_repro'
        if                      _ONLY and test_str[5:] not in _ONLY: return
        DlgAg(
            ctrls=[0
    ,('b1',dict(tp='bttn',cap='Re&name me' ,x=0  ,y=  0    ,w=200))
    ,('l1',dict(tp='labl',cap='>he&re'     ,x=0  ,tid='e1' ,w= 50))
    ,('e1',dict(tp='edit',val='Edit me'    ,x=50 ,y= 30    ,w=150))
    ,('b2',dict(tp='bttn',cap='Sh&ort me'  ,x=0  ,y= 60    ,w=200))
    ,('b3',dict(tp='bttn',cap='A&sk,Close' ,x=0  ,y= 90    ,w=200))
    ,('cl',dict(tp='bttn',cap='Close'      ,x=0  ,y=120    ,w=200,def_bt=1))
                  ][1:]
        ,   form=dict(cap=test_str               ,h=150    ,w=200)
        ,   fid='e1'    # Start focus
                                ,opts=dict(gen_repro_to_file='test_repro_ag.py')
        ).show()
        self.assertTrue(True)


    ##############################
    def test_ag_dict(self):
        test_str= 'test_ag_dict'
        if                      _ONLY and test_str[5:] not in _ONLY: return
        DlgAg(
            ctrls=dispose(dict(_=0
    ,l1=dict(tp='labl'  ,cap='>====' ,x= 0  ,tid='e1' ,w= 50)
    ,e1=dict(tp='edit'  ,val='=====' ,x=50  ,y=  0    ,w=150)
                          ),'_')
        ,   form=dict(cap=test_str          ,h=150   ,w=200)
        ).show()


    ##############################
    def test_ag_border(self):
        test_str= 'test_ag_border'
        if                      _ONLY and test_str[5:] not in _ONLY: return
        ctrls=dict( l1=dict(tp='labl'  ,cap='>====' ,x=20   ,tid='e1'   ,w= 50)
                ,   e1=dict(tp='edit'  ,val='=====' ,x=70   ,y= 10      ,w=400, a='r>')
                ,   ms=dict(tp='labl'               ,x=20   ,y= 40      ,w=480, a='--||', au=True
                                       ,cap='DEFAULT non-resizable border'))
        form=dict(cap=test_str                              ,h= 90      ,w=500)
        
#       DlgAg(ctrls=ctrls, form=form).show(modal=False)         # Default dialog border
        
        # Core API borders
        ctrls['ms']['cap']  = 'DEFAULT resizable border'
#       form['frame']       = 'resize'
#       DlgAg(ctrls=ctrls, form=form).show()
#       DlgAg(ctrls=ctrls, form=form).gen_repro_code('test_repro_ag_border.py')
#       DlgAg(ctrls=ctrls, form=form).gen_repro_code(True)
        
        tbrds   = dispose({0:0
#                   ,app.DBORDER_NONE    : 'DBORDER_NONE     No visible border, not resizable'
#                   ,app.DBORDER_SIZE    : 'DBORDER_SIZE     Standard resizable border'
#                   ,app.DBORDER_SINGLE  : 'DBORDER_SINGLE   Single-line border, not resizable'
                    ,app.DBORDER_DIALOG  : 'DBORDER_DIALOG   Standard dialog box border, not resizable'
#                   ,app.DBORDER_TOOL    : 'DBORDER_TOOL     Single-line border, not resizable with a smaller caption'
#                   ,app.DBORDER_TOOLSIZE: 'DBORDER_TOOLSIZE Standard resizable border with a smaller caption'
                    }, 0)
        for brdc, brds in tbrds.items():
            ctrls['ms']['cap']  = brds
            form['border']      = brdc
            DlgAg(ctrls=ctrls, form=form).show(modal=False)
#           DlgAg(ctrls=ctrls, form=form).gen_repro_code('test_repro_ag_border.py')

        # DlgAg borders
        del form['border']
        frms    = [0
                ,   'no'
                ,   'resize'
#               ,   'full-cap'
                ,   'min-max'
                ][1:]
        for frm in powerset(frms):
            frm    = ','.join(frm)
#       for frm in frms:
            ctrls['ms']['cap']  = f('frame = {}', frm)
            form['frame']       = frm
#           DlgAg(ctrls=ctrls, form=form).show(modal=True)
    
    
    ##############################
    def test_ag_dock(self):
        test_str= 'test_ag_dock'
        if                      _ONLY and test_str[5:] not in _ONLY: return
#       agP=DlgAg(
#           ctrls=[0
#   ,('l1',dict(tp='labl'  ,cap='Parent dlg',x= 0   ,y=0    ,w=100  ,a='--'))
#                 ][1:]
#       ,   form=dict(cap=test_str                  ,h=150  ,w=200)
##                               ,opts=dict(gen_repro_to_file='test_repro_dock_p.py')
#       )
        def acts(ag, name, data=''):
            pass;              #log("ag.val('c1')={}",(ag.val('c1')))
            ag.dock(undock=not ag.val('c1'), side='t')
#           ag.dock(ag_parent=agP, undock=ag.val('c1'))
#           ag.show(modal=False)   # ?
            return []
        agK=DlgAg(
            ctrls=[0
    ,('l1',dict(tp='labl'  ,cap='Kid dlg'   ,x= 0   ,y= 0   ,w= 50  ,a='--'                 ))
    ,('c1',dict(tp='chck'  ,cap='Docked'    ,x= 0   ,y=30   ,w= 70  ,val=False,on=acts      ))
    ,('cl',dict(tp='bttn'  ,cap='Close'     ,x=90   ,y=30   ,w= 50            ,on=CB_HIDE   ))
                  ][1:]
        ,   form=dict(cap='Kid dlg'                 ,h=60   ,w=200)
#                               ,opts=dict(gen_repro_to_file='test_repro_dock_k.py')
        )
#       agK.dock(side='t')
#       agK.dock(agP)
        agK.show(modal=False)
#       agK.show(modal=False)   # Unfortunately need
#       agP.show()


    ##############################
    def test_ag_onetime_nonmodal(self):
        test_str= 'test_ag_onetime_nonmodal'
        if                      _ONLY and test_str[5:] not in _ONLY: return
        ag=DlgAg(
            ctrls=[0
    ,('l1',dict(tp='labl'  ,cap='>====' ,x= 0  ,tid='e1' ,w= 50))
    ,('e1',dict(tp='edit'  ,val='=====' ,x=50  ,y=  0    ,w=150))
                  ][1:]
        ,   form=dict(cap=test_str          ,h=150   ,w=200)
                               #,opts=dict(gen_repro_to_file='test_repro_ag.py')
        )
        ag.show(onetime=False)
        pass;                  #log('')
        ag.show(modal=False)
        pass;                  #log('')


    ##############################
    def test_ag_reset(self):
        test_str= 'test_ag_reset'
        if                      _ONLY and test_str[5:] not in _ONLY: return
        def reset_to(ag, dlg):
            return ag.reset(**dlg)
        dlg1    = dict(
            ctrls=[0
    ,('l11',dict(tp='labl'  ,cap='>===1' ,x= 0  ,tid='e11',w= 50))
    ,('e11',dict(tp='edit'  ,val='====1' ,x=50  ,y=  0    ,w=150))
    ,('b11',dict(tp='bttn'  ,cap='show2' ,x=10  ,y=  30   ,w=180, on=lambda ag,name,data='':reset_to(ag, dlg2)))
                  ][1:]
        ,   form=dict(cap=test_str+'-1'         ,h=150    ,w=200)
        ,   fid='b11'
        )
        dlg2    = dict(
            ctrls=[0
    ,('l21',dict(tp='labl'  ,cap='>===2' ,x= 0  ,tid='e21',w= 50))
    ,('e21',dict(tp='edit'  ,val='====2' ,x=50  ,y=  0    ,w=150))
    ,('b21',dict(tp='bttn'  ,cap='show1' ,x=10  ,y=  30   ,w=200, on=lambda ag,name,data='':reset_to(ag, dlg1)))
                  ][1:]
        ,   form=dict(cap=test_str+'-2'         ,h=170    ,w=220)
        ,   fid='b21'
        )
        ag=DlgAg(**dlg1)
        ag.show(onetime=False)
        ag.reset(**dlg2)
#       ag.gen_repro_code('test_repro_ag.py')
        ag.show()


    ##############################
#   def test_ag_tid(self):
#       test_str= 'test_ag_tid'
#       if                      _ONLY_HAS not in test_str: return 
#       if                      _ONLY_LIST and test_str[5:] not in _ONLY_LIST: return 
#       DlgAg(
#           ctrls=[0
#   ,('l1',dict(tp='labl',cap='>====' ,x= 0 ,tid='e1' ,w= 50))
#   ,('e1',dict(tp='edit',val='=====' ,x=50 ,y=  0    ,w=150))
#                 ][1:]
#       ,   form=dict(cap='test_ag_tid'                ,h=150      ,w=200)
#       ).show()
#       DlgAg(
#           ctrls=[0
#   ,('l1',dict(tp='labl',cap='>====' ,x= 0 ,y=0     ,w= 50))
#   ,('e1',dict(tp='edit',val='=====' ,x=50 ,y=0     ,w=150))
#                 ][1:]
#       ,   form=dict(cap='test_ag_tid'     ,h=150   ,w=200)
#       ).show()
#       self.assertTrue(True)
#
