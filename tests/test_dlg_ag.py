import unittest

import os, tempfile, itertools
from cuda_kv_base import *
from cuda_kv_dlg import *

# test_ag_1
# test_ag_pos
# test_ag_anchor
# test_ag_menu
# test_ag_repro
# test_ag_dict
# test_ag_dock
# test_ag_onetime_nonmodal
# test_ag_reset
# test_ag_tid
pass;                          #_ONLY_HAS = ''              # Only names with the str
pass;                           _ONLY_HAS = 'ag_menu'        # Only names with the str
pass;                          #_ONLY_HAS = 'ag_border'        # Only names with the str
pass;                           _ONLY_LIST= []              # Only names from the list
pass;                          #_ONLY_LIST= ['ag_dict']     # Only names from the list

def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return itertools.chain.from_iterable(itertools.combinations(s, r) for r in range(len(s)+1))

class TestDlgAg(unittest.TestCase):


    ##############################
    def test_ag_1(self):
        # Controls: label, edit, button
        # Tricks: tid, >, def_bttn, call, update, hide, on_exit, cattr, cval, fid
        test_str    = 'test_ag_1'
        if                      _ONLY_HAS  and _ONLY_HAS not in test_str: return 
        if                      _ONLY_LIST and test_str[5:] not in _ONLY_LIST: return 
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
    ,('cl',dict(tp='bttn',cap='Close'      ,x= 0 ,y=120    ,w=200  ,on=CB_HIDE   ,def_bttn=1))
                  ][1:]
        ,   form=dict(cap=test_str               ,h=150    ,w=200)
        ,   fid='e1'    # Start focus
        )
        (rt,vs) = ag.show(do_exit)
        pass;                   log('rt,vs={}',(rt,vs))
        pass;                  #log('val4edit={}',(val4edit))
        self.assertTrue(True)


    ##############################
    def test_ag_pos(self):
        test_str= 'test_ag_pos'
        if                      _ONLY_HAS not in test_str: return 
        if                      _ONLY_LIST and test_str[5:] not in _ONLY_LIST: return 
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
                     ,resize=True)
        ,   fid='edit1'    # Start focus
        ).show()
        self.assertTrue(True)


    ##############################
    def test_ag_anchor(self):
        test_str= 'test_ag_anchor'
        if                      _ONLY_HAS not in test_str: return 
        if                      _ONLY_LIST and test_str[5:] not in _ONLY_LIST: return 
        DlgAg(
            ctrls=[0
    ,('b1',dict(tp='bttn',cap='def'     ,x=  0  ,w=100  ,y=  0              ))
    ,('l1',dict(tp='labl',cap='>def'    ,x=110  ,w= 40  ,tid='e1'           ))
    ,('e1',dict(tp='edit',val='r>'      ,x=150  ,w= 50  ,y=  0              ,a='r>'))
#   ,('b2',dict(tp='bttn',cap='--'      ,x= 50  ,w= 80  ,y= 60              ,a='--'))
    ,('b3',dict(tp='bttn',cap='--'     ,_x=  0  ,w=100  ,y= 30              ,a='--'))
    ,('m1',dict(tp='memo',val='r>b.'    ,x=  0  ,w=100  ,y= 60      ,h=60   ,a='r>b.'))
    ,('m2',dict(tp='memo',cap='>>||'    ,x=110  ,w= 90              ,h=50   ,a='>>||'))
    ,('cl',dict(tp='bttn',cap='>>..'    ,x= 90  ,w=110  ,y=130              ,a='>>..'))
                  ][1:]
        ,   form=dict(cap=test_str              ,w=200  ,h=160      
                     ,resize=True)
        ,   fid='e1'    # Start focus
        ).show()
        self.assertTrue(True)


    ##############################
    def test_ag_menu(self):
        test_str= 'test_ag_menu'
        if                      _ONLY_HAS not in test_str: return 
        if                      _ONLY_LIST and test_str[5:] not in _ONLY_LIST: return 
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
            set_all_for_tree(mn_its, 'sub', 'cmd', wnen_menu)       # All nodes have cmd
            where, dx, dy   =(('dxdy', 7+data['x'], 7+data['y'])    # To show near cursor
                                if type(data)==dict else \
                              ('+h', 0, 0)                          # To show under control
                             )
            return ag.show_menu(mn_its
                , name, where, dx, dy
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
        if                      _ONLY_HAS not in test_str: return 
        if                      _ONLY_LIST and test_str[5:] not in _ONLY_LIST: return 
        DlgAg(
            ctrls=[0
    ,('b1',dict(tp='bttn',cap='Re&name me' ,x=0  ,y=  0    ,w=200))
    ,('l1',dict(tp='labl',cap='>he&re'     ,x=0  ,tid='e1' ,w= 50))
    ,('e1',dict(tp='edit',val='Edit me'    ,x=50 ,y= 30    ,w=150))
    ,('b2',dict(tp='bttn',cap='Sh&ort me'  ,x=0  ,y= 60    ,w=200))
    ,('b3',dict(tp='bttn',cap='A&sk,Close' ,x=0  ,y= 90    ,w=200))
    ,('cl',dict(tp='bttn',cap='Close'      ,x=0  ,y=120    ,w=200,def_bttn=1))
                  ][1:]
        ,   form=dict(cap=test_str               ,h=150    ,w=200)
        ,   fid='e1'    # Start focus
                                ,opts=dict(gen_repro_to_file='test_repro_ag.py')
        ).show()
        self.assertTrue(True)


    ##############################
    def test_ag_dict(self):
        test_str= 'test_ag_dict'
        if                      _ONLY_HAS not in test_str: return 
        if                      _ONLY_LIST and test_str[5:] not in _ONLY_LIST: return 
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
        if                      _ONLY_HAS not in test_str: return 
        if                      _ONLY_LIST and test_str[5:] not in _ONLY_LIST: return 
        ctrls=dict( l1=dict(tp='labl'  ,cap='>====' ,x=20   ,tid='e1'   ,w= 50)
                ,   e1=dict(tp='edit'  ,val='=====' ,x=70   ,y= 10      ,w=400, a='r>')
                ,   ms=dict(tp='labl'               ,x=20   ,y= 40      ,w=480, a='--||', au=True
                                       ,cap='DEFAULT non-resizable border'))
        form=dict(cap=test_str                              ,h= 90      ,w=500)
        
#       DlgAg(ctrls=ctrls, form=form).show(modal=False)
        
        ctrls['ms']['cap']  = 'DEFAULT resizable border'
        form['frame']       = 'resize'
#       DlgAg(ctrls=ctrls, form=form).show()
#       DlgAg(ctrls=ctrls, form=form).gen_repro_code('test_repro_ag_border.py')
#       DlgAg(ctrls=ctrls, form=form).gen_repro_code(True)
        
        tbrds   = dispose({0:0
#                   ,app.DBORDER_NONE    : 'DBORDER_NONE     No visible border, not resizable'
#                   ,app.DBORDER_SIZE    : 'DBORDER_SIZE     Standard resizable border'
#                   ,app.DBORDER_SINGLE  : 'DBORDER_SINGLE   Single-line border, not resizable'
                    ,app.DBORDER_DIALOG  : 'DBORDER_DIALOG   Standard dialog box border, not resizable'
                    ,app.DBORDER_TOOL    : 'DBORDER_TOOL     Single-line border, not resizable with a smaller caption'
#                   ,app.DBORDER_TOOLSIZE: 'DBORDER_TOOLSIZE Standard resizable border with a smaller caption'
                    }, 0)
        for brdc, brds in tbrds.items():
            ctrls['ms']['cap']  = brds
            form['border']      = brdc
            DlgAg(ctrls=ctrls, form=form).show(modal=False)
#           DlgAg(ctrls=ctrls, form=form).gen_repro_code('test_repro_ag_border.py')

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
        if                      _ONLY_HAS not in test_str: return 
        if                      _ONLY_LIST and test_str[5:] not in _ONLY_LIST: return 
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
        if                      _ONLY_HAS not in test_str: return 
        if                      _ONLY_LIST and test_str[5:] not in _ONLY_LIST: return 
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
        if                      _ONLY_HAS not in test_str: return 
        if                      _ONLY_LIST and test_str[5:] not in _ONLY_LIST: return 
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
