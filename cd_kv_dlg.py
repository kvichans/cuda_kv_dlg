''' Lib for Plugin
Authors:
    Andrey Kvichansky    (kvichans on github.com)
Version:
    '0.8.02 2019-03-06'
Content
    See github.com/kvichans/cuda_kv_dlg/wiki
ToDo: (see end of file)
'''

import  sys, os, tempfile, json, re
from    time        import perf_counter

import  cudatext        as app
from    cudatext    import ed
import  cudax_lib       as apx
from    cuda_kv_base import *

VERSION     = re.split('Version:', __doc__)[1].split("'")[1]
VERSION_V,  \
VERSION_D   = VERSION.split(' ')

_       = None
try:
    _   = get_translation(__file__) # I18N
except:pass

pass;                           _log4mod = LOG_FREE  # Order log in the module
    
REDUCTIONS  = {
     'labl': 'label'
    ,'lilb': 'linklabel'
    ,'edit': 'edit'
    ,'edtp': 'edit_pwd'
    ,'sped': 'spinedit'
    ,'memo': 'memo'
    ,'bttn': 'button'
    ,'rdio': 'radio'
    ,'chck': 'check'
    ,'chbt': 'checkbutton'
    ,'chgp': 'checkgroup'
    ,'rdgp': 'radiogroup'
    ,'cmbx': 'combo'
    ,'cmbr': 'combo_ro'
    ,'libx': 'listbox'
    ,'clbx': 'checklistbox'
    ,'livw': 'listview'
    ,'clvw': 'checklistview'
    ,'tabs': 'tabs'
    ,'clpn': 'colorpanel'
    ,'imag': 'image'
    ,'flbx': 'filter_listbox'
    ,'flvw': 'filter_listview'
    ,'bvel': 'bevel'
    ,'pnel': 'panel'
    ,'grop': 'group'
    ,'splt': 'splitter'
    ,'pags': 'pages'
    ,'trvw': 'treeview'
    ,'edtr': 'editor'
    ,'stbr': 'statusbar'
    ,'btex': 'button_ex'
    ,'cols': 'columns'
    }

CB_HIDE = lambda ag,name,d='':None     # Control callback to hide dlg

ALI_CL  = app.ALIGN_CLIENT
ALI_LF  = app.ALIGN_LEFT
ALI_RT  = app.ALIGN_RIGHT
ALI_TP  = app.ALIGN_TOP
ALI_BT  = app.ALIGN_BOTTOM
class DlgAg:
    # See github.com/kvichans/cuda_kv_dlg/wiki
    
    def __init__(self, ctrls, form=None, vals=None, fid=None, opts=None):
        """ Create dialog
        """
        pass;                   log4fun=-1==-1  # Order log in the function
        # Fields
        self.opts   = opts.copy() if opts else {}
        
        self.did    = app.dlg_proc(0, app.DLG_CREATE)
        self.ctrls  = None                              # Mem-attrs of all controls {cid:{k:v}}
        self.form   = None                              # Mem-attrs of form         {k:v}
        
        self._setup(ctrls, form, vals, fid)

        self._gen_repro_code()
       #def __init__

    def show(self, on_exit=None):
        """ Show the dialog """
        pass;                   log4fun=-1==-1  # Order log in the function
        ed_caller   = ed
        
        app.dlg_proc(self.did, app.DLG_SHOW_MODAL)
        
        _form_acts('save', did=self.did
                  ,key4store=self.opts.get('form data key'))
        if on_exit and callable(on_exit):
            on_exit(self)
#       self._before_free()
        _dlg_proc(self.did, app.DLG_FREE)
        
        ed_to_focus = self.opts.get('on_exit_focus_to_ed', ed_caller)
        if ed_to_focus:
            ed_to_focus.focus()
       #def show

    ###############
    ## Getters
    ###############
    def focused(self, live=True):
        if not live:    return self.form.get('fid')
        form    = _dlg_proc(self.did
                        , app.DLG_PROP_GET)
        c_ind   = form.get('focused')
        if not find:    return None
        c_pr    = _dlg_proc(self.did, app.DLG_CTL_PROP_GET, index=c_ind)
        if not c_pr:    return None
        return c_pr['name']
       #def focused
    
    def fattr(self, attr, defv=None, live=True):
        """ Return one form property """
        if attr in ('focused', 'fid'):  return self.focused(live)
        pr  = _dlg_proc(self.did
                        , app.DLG_PROP_GET)     if live else    self.form
        pass;                  #log('pr={}',(pr))
        rsp = pr.get(attr, defv)
        return rsp
       #def fattr

    def fattrs(self, attrs=None, live=True):
        """ Return form properties """
        pr  = _dlg_proc(self.did
                        , app.DLG_PROP_GET)     if live else    self.form
        return pr      if not attrs else \
               {attr:(self.focused(live) if attr in ('focused', 'fid') else pr.get(attr)) 
                    for attr in attrs}
       #def fattrs

    def fhandle(self):
        return self.did
    
    def сhandle(self, name):
        return app.dlg_proc(self.did, app.DLG_CTL_HANDLE, name=name)
    
    def cattr(self, name, attr, defv=None, live=True):
        """ Return one the control property """
        live= False if attr in ('type', 'p')    else live       # Unchangable
        pr  = _dlg_proc(self.did
                        , app.DLG_CTL_PROP_GET
                        , name=name)            if live else    self.ctrls[name]
        attr    = REDUCTIONS.get(attr, attr)
        if attr not in pr:  return defv
        rsp = pr[attr]
        if not live:        return rsp
        if attr=='val':     return self._take_val(name, rsp, defv)
        return                     self._take_it_cl(name, attr, rsp, defv)
       #def cattr

    def cattrs(self, name, attrs=None, live=True):
        """ Return the control properties """
        pr  = _dlg_proc(self.did
                        , app.DLG_CTL_PROP_GET
                        , name=name)            if live else    self.ctrls[name]
        attrs   = attrs if attrs else list(pr.keys())
        pass;                  #log('pr={}',(pr))
        rsp     = {attr:pr.get(attr) for attr in attrs 
                    if attr not in ('type', 'p', 'val')}
        if 'val' in attrs:
            rsp['val']  = self._take_val(name, pr.get('val')) if live else pr.get('val')
        if 'p' in attrs:
            rsp['p']    = self.ctrls[name].get('p', '')
        if 'type' in attrs:
            rsp['type'] = self.ctrls[name]['type']
        return rsp
       #def cattrs
       
    def cval(self, name, live=True):
        """ Return the control val property """
        return      self.cattr(name, 'val', defv=None, live=live)
    def cvals(self, names, live=True):
        """ Return the controls val property """
        return {cid:self.cattr(cid, 'val', defv=None, live=live) for cid in names}
    
    def chandle(self, name):
        return app.dlg_proc(self.did, app.DLG_CTL_HANDLE, name=name)


    ###############
    ## Updaters
    ###############
    def update(self, upds):
        """ Update most of dlg props
            upds is dict(ctrls=, form=, vals=, fid=) 
                ctrls   [(name, {k:v})] or {name:{k:v}}
                form    {k:v}
                vals    {name:v}
                fid     name
            Or upds is list of such dicts
        """
        pass;                   log4fun=-1==-1  # Order log in the function
        if upds is None:                                                # To hide/close
            app.dlg_proc(self.did, app.DLG_HIDE)
            return
        if not upds:
            return False                                                # False to cancel the current event
        if isinstance(upds, tuple) or isinstance(upds, list) :          # Allow to use list of upd data
            for upd in upds:
                self.update(upd)
            return 
        cupds   = upds.get('ctrls',  [])
        cupds   = odict(cupds)      if isinstance(cupds, tuple) or isinstance(cupds, list) else cupds
        pass;          #log('cupds={}',(cupds))
        vals    = upds.get('vals', {})
        form    = upds.get('form', {})

        DlgAg._check_data(self.ctrls, cupds, form, vals, upds.get('fid'))

        if False:pass
        elif vals and not cupds:                                        # Allow to update only val in some controls
            cupds     = { cid_    :  {'val':val} for cid_, val in vals.items()}
        elif vals and     cupds:
            for cid_, val in vals.items():
                if cid_ not in cupds:
                    cupds[cid_]   =  {'val':val}                        # Merge vals to cupds
                else:
                    cupds[cid_]['val']    = val                         # NB! val from vals but not from cupds
        for cid_, cfg in cupds.items():
            cfg['tp']   = self.ctrls[cid_]['tp']                        # Type is stable
            cfg['type'] = self.ctrls[cid_]['type']                      # Type is stable

        if form:
            self.form.update(form)
            pass;              #log('form={}',(self.fattrs(live=F)))
            pass;              #log('form={}',(self.fattrs()))
            pass;              #log('form={}',(form))
            _dlg_proc(self.did
                     ,app.DLG_PROP_SET
                     ,prop=form)

        if cupds:
            for cid, new_cfg in cupds.items():
                pass;          #log('cid, new_cfg={}',(cid, new_cfg))
                
                cfg     = self.ctrls[cid]
                cfg.update(new_cfg)
                c_prop  = self._prepare_control_prop(cid, new_cfg, {'ctrls':cupds})
                pass;          #log('c_prop={}',(c_prop)) if new_ctrl['type']=='listview' else None
                _dlg_proc(self.did
                         ,app.DLG_CTL_PROP_SET
                         ,name=cid
                         ,prop=c_prop
                         )

        if 'fid' in upds:
            self.form['fid']    = upds['fid']
            app.dlg_proc(self.did
                        ,app.DLG_CTL_FOCUS
                        ,name=upds['fid'])
       #def update
       
    @staticmethod
    def _check_data(mem_ctrls, ctrls, form, vals, fid):
        # Check cid/tid/fid in (ctrls, form, vals, fid) to exist into mem_ctrls
        if 'skip checks'=='skip checks':    return 
        no_tids = {cnt['tid'] 
                    for cnt in ctrls 
                    if 'tid' in cnt and 
                        cnt['tid'] not in mem_ctrls}
        if no_tids:
            raise ValueError(f('No name for tid: {}', no_tids))

        if 'fid' in form and form['fid'] not in mem_ctrls:
            raise ValueError(f('No name for form[fid]: {}', form['fid']))
        
        no_vals = {cid 
                    for cid in vals 
                    if cid not in mem_ctrls} if vals else None
        if no_vals:
            raise ValueError(f('No name for val: {}', no_vals))
        
        if fid is not None and fid not in mem_ctrls:
            raise ValueError(f('No name for fid: {}', fid))
       #def _check_data
       
    def _setup(self, ctrls, form, vals=None, fid=None):
        """ Arrange and fill all: controls attrs, form attrs, focus.
            Params
                ctrls   [(name, {k:v})] or {name:{k:v}} 
                            NB! Only from 5.7 Python saves key sequence for dict.
                                The sequence is important for tab-order of controls.
                form    {k:v}
                vals    {name:v}
                fid     name
        """
        pass;                   log4fun=-1==-1  # Order log in the function
        #NOTE: DlgAg init
        self.ctrls  = odict(ctrls)  if isinstance(ctrls, tuple) or isinstance(ctrls, list) else ctrls.copy()
        self.form   = form.copy()
        fid         = fid           if fid else form.get('fid', form.get('focused'))
        
        DlgAg._check_data(self.ctrls, ctrls, form, vals, fid)
        
        if vals:
            for cid, val in vals.items():
                self.ctrls[cid]['val']  = val
        
        # Create controls
        for cid, ccfg in self.ctrls.items():
            tp      = ccfg.get('tp',  ccfg.get('type'))
            if not tp:
                raise ValueError(f('No type/tp for name: {}', cid))
            ccfg['tp']      = tp
            ccfg['type']    = REDUCTIONS.get(tp, tp)
            # Create control
            _dlg_proc(self.did
                     ,DLG_CTL_ADD_SET
                     ,name=ccfg['type']
                     ,prop=self._prepare_control_prop(cid, ccfg))
           #for cid, ccfg
        
        # Prepare form
        fpr     = self.form
        fpr['topmost']      = True
        w0      = fpr['w']
        h0      = fpr['h']
        # Prepare callbacks
        def get_proxy_cb(u_callbk, event):
            def ag_callbk(idd, idc=-1, data=''):
                upds    = user_callbk(self)
                if upds:
                    return self.update(upds)
               #def ag_callbk
            return ag_callbk
           #def get_proxy_cb
        for on_key in [k for k in fpr if k[:3]=='on_' and callable(fpr[k])]:
            user_callbk = fpr[on_key]
            fpr[on_key] = get_proxy_cb(user_callbk, on_key)
           #for on_key
        
        # Prepare to resize
        if callable(fpr.get('on_resize')):
            fpr.get['resize']= True
        if fpr.get('resize'):
#           fpr.pop('resize')
#           fpr.get['border']= app.DBORDER_DIALOG
            self._prepare_anchors()                                 # a,aid -> a_*,sp_*
            fpr['w_min']    = fpr.get('w_min', w0)
            fpr['h_min']    = fpr.get('h_min', h0)
        # Restore prev pos/sizes
        fpr     = _form_acts('move', fprs=fpr      # Move and (maybe) resize
                            , key4store=self.opts.get('form data key'))
        _dlg_proc(self.did, app.DLG_PROP_SET, prop=fpr)         # push to live
        if 'on_resize'   in fpr and \
           (fpr['w'],fpr['h']) != (w0,h0):
            pass;              #log('fpr[w],fpr[h],w0,h0={}',(fpr['w'], fpr['h'], w0,h0))
            fpr['on_resize'](self)

        if fid:
            fpr['focused']  = fid                               # save in mem
            app.dlg_proc(self.did, app.DLG_CTL_FOCUS, name=fid) # push to live
       #def _setup

    def _prepare_control_prop(self, cid, ccfg, opts={}):
        pass;                   log4fun=-1== 1  # Order log in the function
        Self    = self.__class__
        pass;                   log('cid, ccfg={}',(cid, ccfg)) if iflog(log4fun,_log4mod) else 0
        EXTRA_C_ATTRS   = ['tp','r','b','tid','a','aid']
        tp      = ccfg['type']
        Self._preprocessor(ccfg, tp)                    # sto -> tab_stop,...         EXTRA_C_ATTRS
        c_pr    = {k:v for (k,v) in ccfg.items()         if k not in ['items', 'val']+EXTRA_C_ATTRS and k[:3]!='on_'}
        c_pr['name'] = cid
        c_pr    = self._prepare_it_vl(c_pr, ccfg, opts) #if k     in ['items', 'val']
        
        c_pr.update(self._prep_pos_attrs(ccfg, cid, opts.get('ctrls')))                    # l,r,t,b,tid -> x,y,w,h
        pass;                   log('c_pr={}',(c_pr)) if iflog(log4fun,_log4mod) else 0
        
        # Prepare callbacks
        def get_proxy_cb(u_callbk, event):
            def ag_callbk(idd, idc, data):
                pass;          #log('ev,idc,cid,data={}',(event,idc,cid,data))
                if tp in ('listview',) and type(data) in (tuple, list):
                    if not data[1]: return  # Skip event "selection loss"
                    # Crutch for Linux! Wait fix in core
                    event_val   = app.dlg_proc(idd, app.DLG_CTL_PROP_GET, index=idc)['val']
                    if event_val!=data[0]:
                        app.dlg_proc(          idd, app.DLG_CTL_PROP_SET, index=idc, prop={'val':data[0]})
                pass;          #log('?? u_callbk',())
                upds    = u_callbk(self, cid, data)
                pass;          #log('ok u_callbk upds={}',(upds))
                pass;          #log('upds={}',(upds))
                return self.update(upds)
               #def ag_callbk
            return ag_callbk
           #def get_proxy_cb
            
        for on_key in [k for k in ccfg if k[:3]=='on_' and callable(ccfg[k])]:
            if tp!='button':
                c_pr['act'] = True
            user_callbk     = ccfg[on_key]
            c_pr[on_key]    = get_proxy_cb(user_callbk, on_key)
           #for on_key
        
        return c_pr
       #def _prepare_control_prop

    def _prep_pos_attrs(self, cnt, cid, ctrls4cid=None):
        pass;                   log4fun=-1== 1  # Order log in the function
        ctrls4cid = ctrls4cid if ctrls4cid else self.ctrls
        reflex  = self.opts.get('negative_coords_reflect', False)
        pass;                   log('cid, reflex, cnt={}',(cid, reflex, cnt)) if iflog(log4fun,_log4mod) else 0
        prP     =  {}

        cnt_ty  = ctrls4cid[cid].get('tp', ctrls4cid[cid].get('type'))
        cnt_ty  = REDUCTIONS.get(cnt_ty, cnt_ty)
        if  cnt_ty in ('label', 'linklabel'
                      ,'combo', 'combo_ro'
                      )         \
        or  'h' not in cnt  and \
            cnt_ty in ('button', 'checkbutton'
                      ,'edit', 'spinedit'
                      ,'check', 'radio'
                      ,'filter_listbox', 'filter_listview'
                      ):
            # OS specific control height
            cnt['h']    = _get_gui_height(cnt_ty)   # type kills h
            prP['_ready_h'] = True                  # Skip scaling
            pass;              #log('cnt={}',(cnt)) if cnt_ty=='checkbutton' else 0

        if 'tid' in cnt:
            assert cnt['tid'] in ctrls4cid
            # cid for horz-align text
            bas_cnt     = ctrls4cid[ cnt['tid']]
            bas_ty      = bas_cnt.get('tp', bas_cnt.get('type'))
            bas_ty      = REDUCTIONS.get(bas_ty, bas_ty)
            t           = bas_cnt.get('y', 0) + _fit_top_by_env(cnt_ty, bas_ty)
            cnt['y']    = t          # tid kills y
        
        if reflex: #NOTE: reflex
            def do_reflex(cnt_, k, pval):
                if 0>cnt_.get(k, 0):
                    pass;       log('cid, k, pval, cnt_={}',(cid, k, pval, cnt_)) if iflog(log4fun,_log4mod) else 0
                    cnt_[k]    = pval + cnt_[k]
                    pass;       log('cnt_={}',(cnt_)) if iflog(log4fun,_log4mod) else 0
            prnt    = cnt.get('p', self.form)
            prnt_w  = prnt.get('w', 0) 
            prnt_h  = prnt.get('h', 0)
            pass;               log('prnt={}',(prnt)) if iflog(log4fun,_log4mod) else 0
            pass;               log('prnt_w,prnt_h={}',(prnt_w,prnt_h)) if iflog(log4fun,_log4mod) else 0
            pass;               log('cnt={}',(cnt)) if iflog(log4fun,_log4mod) else 0
            do_reflex(cnt, 'x', prnt_w)
            do_reflex(cnt, 'r', prnt_w)
            do_reflex(cnt, 'y', prnt_h)
            do_reflex(cnt, 'b', prnt_h)
            pass;               log('cnt={}',(cnt)) if iflog(log4fun,_log4mod) else 0

        def calt_third(kasx, kasr, kasw, src, trg):
            # Use d[kasw] = d[kasr] - d[kasx]
            #   to copy val from src to trg
            # Skip kasr if it is redundant
            if False:pass
            elif kasx in src and kasw in src:     # x,w or y,h is enough
                trg[kasx]   = src[kasx]
                trg[kasw]   = src[kasw]
            elif kasr in src and kasw in src:     # r,w or b,h to calc
                trg[kasx]   = src[kasw] - src[kasr]
                trg[kasw]   = src[kasw]
            elif kasx in src and kasr in src:     # x,r or y,b to calc
                trg[kasx]   = src[kasx]
                trg[kasw]   = src[kasr] - src[kasx]
            return trg
           #def calt_third
        
        prP = calt_third('x', 'r', 'w', cnt, prP)
        prP = calt_third('y', 'b', 'h', cnt, prP)
#       for k in ('x', 'y'):
#           if k in cnt:
#               prP[k]  = cnt[k]
#       if 'r' in cnt and 'x' in prP:
#           prP['w']    = cnt['r'] - prP['x']   # r,x   kill w
#       if 'w' in cnt:
#           prP['w']    = cnt['w']
#       if 'r' in cnt and 'w' in prP:
#           prP['x']    = cnt['r'] - prP['w']   # r,x   kill w
#
#       if 'b' in cnt and 'y' in prP:
#           prP['h']    = cnt['b'] - prP['y']
#       if 'h' in cnt:
#           prP['h']    = cnt['h']
        pass;                  #log('cid, prP={}',(cid, prP))
        return prP
       #def _prep_pos_attrs

    def _prepare_it_vl(self, c_pr, cfg_ctrl, opts={}):
        pass;                   log4fun=-1==-1  # Order log in the function
        tp      = cfg_ctrl['type']

        if 'val' in cfg_ctrl        and opts.get('prepare val', True):
            in_val  = cfg_ctrl['val']
            if False:pass
            elif tp=='memo':
                # For memo: "\t"-separated lines (in lines "\t" must be replaced to chr(2)) 
                if isinstance(in_val, list):
                    in_val = '\t'.join([v.replace('\t', chr(2)) for v in in_val])
                else:
                    in_val = in_val.replace('\t', chr(2)).replace('\r\n','\n').replace('\r','\n').replace('\n','\t')
            elif tp=='checkgroup' and isinstance(in_val, list):
                # For checkgroup: ","-separated checks (values "0"/"1") 
                in_val = ','.join(in_val)
            elif tp in ['checklistbox', 'checklistview'] and isinstance(in_val, tuple):
                # For checklistbox, checklistview: index+";"+checks 
                in_val = ';'.join( (str(in_val[0]), ','.join( in_val[1]) ) )
            c_pr['val']     = in_val

        if 'items' in cfg_ctrl        and opts.get('prepare items', True):
            items   = cfg_ctrl['items']
            if isinstance(items, str):
                pass
            elif tp in ['listview', 'checklistview']:
                # For listview, checklistview: "\t"-separated items.
                #   first item is column headers: title1+"="+size1 + "\r" + title2+"="+size2 + "\r" +...
                #   other items are data: cell1+"\r"+cell2+"\r"+...
                # ([(hd,wd)], [[cells],[cells],])
                items   = '\t'.join(['\r'.join(['='.join((hd,sz)) for hd,sz in items[0]])]
                                   +['\r'.join(row) for row in items[1]]
                                   )
            else:
                # For combo, combo_ro, listbox, checkgroup, radiogroup, checklistbox: "\t"-separated lines
                items   = '\t'.join(items)
            c_pr['items']   = items

        if 'cols' in cfg_ctrl        and opts.get('prepare cols', True):
            cols   = cfg_ctrl['cols']
            cfg_ctrl['columns'] = cols
            if isinstance(cols, str):
                pass
            else:
                # For listview, checklistview: 
                #   "\t"-separated of 
                #       "\r"-separated 
                #           Name, Width, Min Width, Max Width, Alignment (str), Autosize('0'/'1'), Visible('0'/'1')
                pass;          #log('cols={}',(cols))
                str_sc = lambda n: str(_os_scale('scale', {'w':n})['w'])
                cols   = '\t'.join(['\r'.join([       cd[    'nm']
#                                             ,str(   cd[    'wd']   )
#                                             ,str(   cd.get('mi' ,0))
#                                             ,str(   cd.get('ma' ,0))
                                              ,str_sc(cd[    'wd']   )
                                              ,str_sc(cd.get('mi' ,0))
                                              ,str_sc(cd.get('ma' ,0))
                                              ,       cd.get('al','')
                                              ,'1' if cd.get('au',False) else '0'
                                              ,'1' if cd.get('vi',True) else '0'
                                              ])
                                    for cd in cols]
                                  )
                pass;          #log('cols={}',repr(cols))
            c_pr['columns'] = cols
            pass;              #log('isinstance(cfg_ctrl[columns], str)={}',(isinstance(cfg_ctrl['columns'], str)))

        return c_pr
       #def _prepare_it_vl

    def _take_val(self, name, liv_val, defv=None):
        tp      = self.ctrls[name]['type']
        old_val = self.ctrls[name].get('val', defv)
        new_val = liv_val
        if False:pass
        elif tp=='memo':
            # For memo: "\t"-separated lines (in lines "\t" must be replaced to chr(2)) 
            if isinstance(old_val, list):
                new_val = [v.replace(chr(2), '\t') for v in liv_val.split('\t')]
               #liv_val = '\t'.join([v.replace('\t', chr(2)) for v in old_val])
            else:
                new_val = liv_val.replace('\t','\n').replace(chr(2), '\t')
               #liv_val = old_val.replace('\t', chr(2)).replace('\r\n','\n').replace('\r','\n').replace('\n','\t')
        elif tp=='checkgroup' and isinstance(old_val, list):
            # For checkgroup: ","-separated checks (values "0"/"1") 
            new_val = liv_val.split(',')
           #in_val = ','.join(in_val)
        elif tp in ['checklistbox', 'checklistview'] and isinstance(old_val, tuple):
            new_val = liv_val.split(';')
            new_val = (new_val[0], new_val[1].split(','))
           #liv_val = ';'.join(old_val[0], ','.join(old_val[1]))
        elif isinstance(old_val, bool): 
            new_val = liv_val=='1'
        elif tp=='listview':
            new_val = -1 if liv_val=='' else int(liv_val)
        elif old_val is not None: 
            pass;              #log('name,old_val,liv_val={}',(name,old_val,liv_val))
            new_val = type(old_val)(liv_val)
        return new_val
       #def _take_val

    def _take_it_cl(self, name, attr, liv_val, defv=None):
        tp      = self.ctrls[name]['type']
        old_val = self.ctrls[name].get(attr, defv)
        pass;                  #log('name, attr, isinstance(old_val, str)={}',(name, attr, isinstance(old_val, str)))
        if isinstance(old_val, str):
            # No need parsing - config was by string
            return liv_val
        new_val = liv_val
        
        if attr=='items':
            if tp in ['listview', 'checklistview']:
                # For listview, checklistview: "\t"-separated items.
                #   first item is column headers: title1+"="+size1 + "\r" + title2+"="+size2 + "\r" +...
                #   other items are data: cell1+"\r"+cell2+"\r"+...
                # ([(hd,wd)], [[cells],[cells],])
                header_rows = new_val.split('\t')
                new_val =[[h.split('=')  for h in header_rows[0].split('\r')]
                         ,[r.split('\r') for r in header_rows[1:]]
                         ]
            else:
                # For combo, combo_ro, listbox, checkgroup, radiogroup, checklistbox: "\t"-separated lines
                new_val     = new_val.split('\t')
        
        if attr=='columns':
            # For listview, checklistview: 
            #   "\t"-separated of 
            #       "\r"-separated 
            #           Name, Width, Min Width, Max Width, Alignment (str), Autosize('0'/'1'), Visible('0'/'1')
            # [{nm:str, wd:num, mi:num, ma:num, al:str, au:bool, vi:bool}]
            pass;              #log('new_val={}',repr(new_val))
            new_val= [ci.split('\r')      for ci in new_val.split('\t')]
#           new_val= [ci.split('\r')[:-1] for ci in new_val.split('\t')[:-1]]   # API bug
            pass;              #log('new_val={}',repr(new_val))
            int_sc = lambda s: _os_scale('unscale', {'w':int(s)})['w']
            new_val= [dict(nm=       ci[0]
#                         ,wd=int( ci[1])
#                         ,mi=int( ci[2])
#                         ,ma=int( ci[3])
                          ,wd=int_sc(ci[1])
                          ,mi=int_sc(ci[2])
                          ,ma=int_sc(ci[3])
                          ,au='1'==  ci[4]
                          ,vi='1'==  ci[5]
                          ) for ci in new_val]
            pass;              #log('new_val={}',(new_val))
        
        return new_val
       #def _take_it_cl

    @staticmethod
    def _preprocessor(cnt, tp):
        pass;                   log4fun=-1== 1  # Order log in the function
        pass;                   log('tp,cnt={}',(tp,cnt)) if iflog(log4fun,_log4mod) else 0
        # call -> on_???
        if 'on' in cnt:
            if False:pass
            elif tp in ('listview', 'treeview'):
                cnt['on_select']    = cnt['on']
            elif tp in ('linklabel'):
                cnt['on_click']     = cnt['on']
            else:
                cnt['on_change']    = cnt['on']

        # Reductions
        if 'ali' in cnt:
            cnt['align'] = cnt.pop('ali')                               # ali -> align
        if 'sp_lr' in cnt:
            cnt['sp_l'] = cnt['sp_r']               = cnt.pop('sp_lr')
        if 'sp_lrt' in cnt:
            cnt['sp_l'] = cnt['sp_r'] = cnt['sp_t'] = cnt.pop('sp_lrt')
        if 'sp_lrb' in cnt:
            cnt['sp_l'] = cnt['sp_r'] = cnt['sp_b'] = cnt.pop('sp_lrb')

        cnt['autosize'] = False
        if 'au' in cnt:
            cnt['autosize'] = cnt.pop('au')                             # au -> autosize
        if 'sto' in cnt:
            cnt['tab_stop'] = cnt.pop('sto')                            # sto -> tab_stop
        if 'tor' in cnt:
            cnt['tab_order'] = cnt.pop('tor')                           # tor -> tab_order
        
        # Move smth to props
        if 'props' in cnt:
            pass
        elif tp=='label' and 'cap' in cnt and cnt['cap'][0]=='>':       # cap='>smth' -> cap='smth', props='1' (r-align)
            cnt['cap']  = cnt['cap'][1:]
            cnt['props']= '1'
        elif tp=='label' and    cnt.get('ralign'):                      # ralign -> props
            cnt['props']=       cnt.pop('ralign')
        elif tp=='button' and cnt.get('def_bttn') in ('1', True):       # def_bttn -> props
            cnt['props']= '1'
        elif tp=='button' and cnt.get('def_bt') in ('1', True):         # def_bt -> props
            cnt['props']= '1'
        elif tp=='spinedit' and cnt.get('min_max_inc'):                 # min_max_inc -> props
            cnt['props']=       cnt.pop('min_max_inc')
        elif tp=='linklabel' and    cnt.get('url'):                     # url -> props
            cnt['props']=           cnt.pop('url')
        elif tp=='listview' and cnt.get('grid'):                        # grid -> props
            cnt['props']=       cnt.pop('grid')
        elif tp=='tabs' and     cnt.get('at_botttom'):                  # at_botttom -> props
            cnt['props']=       cnt.pop('at_botttom')
        elif tp=='colorpanel' and   cnt.get('brdW_fillC_fontC_brdC'):   # brdW_fillC_fontC_brdC -> props
            cnt['props']=           cnt.pop('brdW_fillC_fontC_brdC')
        elif tp in ('edit', 'memo') and cnt.get('ro_mono_brd'):         # ro_mono_brd -> props
            cnt['props']=               cnt.pop('ro_mono_brd')

        if 'props' in cnt and app.app_api_version()>='1.0.224':
            # Convert props to ex0..ex9
            #   See 'Prop "ex"' at wiki.freepascal.org/CudaText_API
            lsPr = cnt.pop('props').split(',')
            pass;               log('lsPr={}',(lsPr)) if iflog(log4fun,_log4mod) else 0
            if False:pass
            elif tp=='button':
                cnt['ex0']  = '1'==lsPr[0]  #bool: default for Enter key
            elif tp in ('edit', 'memo'):
                cnt['ex0']  = '1'==lsPr[0]  #bool: read-only
                cnt['ex1']  = '1'==lsPr[1]  #bool: font is monospaced
                cnt['ex2']  = '1'==lsPr[2]  #bool: show border
            elif tp=='spinedit':
                cnt['ex0']  =  int(lsPr[0]) #int:  min value
                cnt['ex1']  =  int(lsPr[1]) #int:  max value
                cnt['ex2']  =  int(lsPr[2]) #int:  increment
            elif tp=='label':
                cnt['ex0']  = '1'==lsPr[0]  #bool: right aligned
            elif tp=='linklabel':
                cnt['ex0']  = lsPr[0]       #str: URL. Should not have ','. Clicking on http:/mailto: URLs should work, result of clicking on other kinds depends on OS.
            elif tp=='listview':
                cnt['ex0']  = '1'==lsPr[0]  #bool: show grid lines
            elif tp=='tabs':
                cnt['ex0']  = '1'==lsPr[0]  #bool: show tabs at bottom
            elif tp=='colorpanel':
                cnt['ex0']  =  int(lsPr[0]) #int:  border width (from 0)
                cnt['ex1']  =  int(lsPr[1]) #int:  color of fill
                cnt['ex2']  =  int(lsPr[2]) #int:  color of font
                cnt['ex3']  =  int(lsPr[3]) #int:  color of border
            elif tp=='filter_listview':
                cnt['ex0']  = '1'==lsPr[0]  #bool: filter works for all columns
            elif tp=='image':
                cnt['ex0']  = '1'==lsPr[0]  #bool: center picture
                cnt['ex1']  = '1'==lsPr[1]  #bool: stretch picture
                cnt['ex2']  = '1'==lsPr[2]  #bool: allow stretch in
                cnt['ex3']  = '1'==lsPr[3]  #bool: allow stretch out
                cnt['ex4']  = '1'==lsPr[4]  #bool: keep origin x, when big picture clipped
                cnt['ex5']  = '1'==lsPr[5]  #bool: keep origin y, when big picture clipped
            elif tp=='trackbar':
                cnt['ex0']  =  int(lsPr[0]) #int:  orientation (0: horz, 1: vert)
                cnt['ex1']  =  int(lsPr[1]) #int:  min value
                cnt['ex2']  =  int(lsPr[2]) #int:  max value
                cnt['ex3']  =  int(lsPr[3]) #int:  line size
                cnt['ex4']  =  int(lsPr[4]) #int:  page size
                cnt['ex5']  = '1'==lsPr[5]  #bool: reversed
                cnt['ex6']  =  int(lsPr[6]) #int:  tick marks position (0: bottom-right, 1: top-left, 2: both)
                cnt['ex7']  =  int(lsPr[7]) #int:  tick style (0: none, 1: auto, 2: manual)
            elif tp=='progressbar':
                cnt['ex0']  =  int(lsPr[0]) #int:  orientation (0: horz, 1: vert, 2: right-to-left, 3: top-down)
                cnt['ex1']  =  int(lsPr[1]) #int:  min value
                cnt['ex2']  =  int(lsPr[2]) #int:  max value
                cnt['ex3']  = '1'==lsPr[3]  #bool: smooth bar
                cnt['ex4']  =  int(lsPr[4]) #int:  step
                cnt['ex5']  =  int(lsPr[5]) #int:  style (0: normal, 1: marquee)
                cnt['ex6']  = '1'==lsPr[6]  #bool: show text (only for some OSes)
            elif tp=='progressbar_ex':
                cnt['ex0']  =  int(lsPr[0]) #int:  style (0: text only, 1: horz bar, 2: vert bar, 3: pie, 4: needle, 5: half-pie)
                cnt['ex1']  =  int(lsPr[1]) #int:  min value
                cnt['ex2']  =  int(lsPr[2]) #int:  max value
                cnt['ex3']  = '1'==lsPr[3]  #bool: show text
                cnt['ex4']  =  int(lsPr[4]) #int:  color of background
                cnt['ex5']  =  int(lsPr[5]) #int:  color of foreground
                cnt['ex6']  =  int(lsPr[6]) #int:  color of border
            elif tp=='bevel':
                cnt['ex0']  =  int(lsPr[0]) #int:  shape (0: sunken panel, 1: 4 separate lines - use it as border for group of controls, 2: top line, 3: bottom line, 4: left line, 5: right line, 6: no lines, empty space)
            elif tp=='splitter':
                cnt['ex0']  = '1'==lsPr[0]  #bool: beveled style
                cnt['ex1']  = '1'==lsPr[1]  #bool: instant repainting
                cnt['ex2']  = '1'==lsPr[2]  #bool: auto snap to edge
                cnt['ex3']  =  int(lsPr[3]) #int:  min size
        pass;                   log('cnt={}',(cnt)) if iflog(log4fun,_log4mod) else 0
       #def _preprocessor

    def _prepare_anchors(self):
        """ Translate attrs 'a' 'aid' to 'a_*','sp_*'
            Values for 'a' are str-mask with signs
                'l<' 'l>'    fixed distanse ctrl-left     to trg-left  or trg-right
                'r<' 'r>'    fixed distanse ctrl-right    to trg-left  or trg-right
                't^' 't.'    fixed distanse ctrl-top      to trg-top   or trg-bottom
                'b^' 'b.'    fixed distanse ctrl-bottom   to trg-top   or trg-bottom
        """
        fm_w    = self.form['w']
        fm_h    = self.form['h']
        for cid,cnt in self.ctrls.items():
            anc     = cnt.get('a'  , '')
            if not anc: continue
            aid     = cnt.get('aid', cnt.get('p', ''))    # '' anchor to form
            trg_w,  \
            trg_h   = fm_w, fm_h
            if aid in self.ctrls:
                prTrg   = _dlg_proc(self.did, app.DLG_CTL_PROP_GET, name=aid)
                trg_w,  \
                trg_h   = prTrg['w'], prTrg['h']
            prOld   = _dlg_proc(self.did, app.DLG_CTL_PROP_GET, name=cid)
            pass;               logb=cid in ('tolx', 'tofi')
            pass;              #nat_prOld=app.dlg_proc(self.did, app.DLG_CTL_PROP_GET, name=cid)
            pass;              #log('cid,nat-prOld={}',(cid,{k:v for k,v in nat_prOld.items() if k in ('x','y','w','h','_ready_h')})) if logb else 0
            pass;              #log('cid,    prOld={}',(cid,{k:v for k,v in     prOld.items() if k in ('x','y','w','h','_ready_h')})) if logb else 0
            pass;              #log('cid,anc,trg_w,trg_h,prOld={}',(cid,anc,trg_w,trg_h, {k:v for k,v in prOld.items() if k in ('x','y','w','h')})) \
                               #    if logb else 0
            prAnc   = {}
            l2r     = 'l>' in anc or '>>' in anc
            r2r     = 'r>' in anc or '>>' in anc
            t2b     = 't.' in anc or '..' in anc
            b2b     = 'b.' in anc or '..' in anc
            if False:pass
            elif '--' in anc:           # h-center
                prAnc.update(dict( a_l=(aid, '-')
                                  ,a_r=(aid, '-')))
            elif not l2r and not r2r:   # Both to left
                pass # def
            elif     l2r and     r2r:   # Both to right
                pass;          #log('l> r>') if logb else 0
                prAnc.update(dict( a_l=None                                             # (aid, ']'), sp_l=trg_w-prOld['x']
                                  ,a_r=(aid, ']'), sp_r=trg_w-prOld['x']-prOld['w']))
            elif     l2r and not r2r:   # Left to right
                pass;          #log('l> r<') if logb else 0
                prAnc.update(dict( a_l=(aid, '['), sp_l=trg_w-prOld['x']
                                  ,a_r=None))
            elif not l2r and     r2r:   # Right to right.
                pass;          #log('l< r>') if logb else 0
                prAnc.update(dict( a_l=(aid, '['), sp_l=      prOld['x']
                                  ,a_r=(aid, ']'), sp_r=trg_w-prOld['x']-prOld['w']))
            
            if False:pass
            elif '||' in anc:           # v-center
                prAnc.update(dict( a_t=(aid, '-')
                                  ,a_b=(aid, '-')))
            elif not t2b and not b2b:   # Both to top
                pass # def
            elif     t2b and     b2b:   # Both to bottom
                pass;          #log('t. b.') if logb else 0
                prAnc.update(dict( a_t=None      #, sp_t=trg_h-prOld['y']                # a_t=(aid, ']') - API bug
                                  ,a_b=(aid, ']'), sp_b=trg_h-prOld['y']-prOld['h']))
            elif     t2b and not b2b:   # Top to bottom
                pass;          #log('t. b^') if logb else 0
                prAnc.update(dict( a_t=(aid, ']'), sp_t=trg_h-prOld['y']                # a_t=(aid, ']') - API bug
                                  ,a_b=None))
            elif not t2b and     b2b:   # Bottom to bottom.
                pass;          #log('t^ b.') if logb else 0
                prAnc.update(dict( a_t=(aid, '['), sp_t=      prOld['y']
                                  ,a_b=(aid, ']'), sp_b=trg_h-prOld['y']-prOld['h']))
            
            if prAnc:
                pass;          #log('aid,prAnc={}',(cid, prAnc)) if logb else 0
                cnt.update(prAnc)
                _dlg_proc(self.did, app.DLG_CTL_PROP_SET, name=cid, prop=prAnc)
#               pass;           pr_   = _dlg_proc(self.did, app.DLG_CTL_PROP_GET, name=cid)
#               pass;           log('cid,pr_={}',(cid, {k:v for k,v in pr_.items() if k in ('h','y', 'sp_t', 'sp_b', 'a_t', 'a_b')}))
       #def _prepare_anchors

    def show_menu(self, mn_content, name, where='+h', dx=0, dy=0, repro_to_file=None):
        """ mn_content      [{cap:'', tag:'', en:T, mark:''|'c'|'r', cmd:(lambda ag, tag:''), sub:[]}]
            name            Control to show menu near it
            where           Menu position 
                                '+h'    - under the control
                                '+w'    - righter the control
                                'dxdy'  - to use dx, dy 
            repro_to_file   File name (w/o path) to write reprocode with only menu_proc 
        """
        pr      = self.cattrs(name, ('x','y','w','h', 'p'))
        pid     = pr['p']
        while pid:
            ppr = self.cattrs(pid, ('x','y', 'p'))
            pass;              #log('pid, ppr={}',())
            pr['x']+= ppr['x']
            pr['y']+= ppr['y']
            pid     = ppr['p']
        x, y    =  pr['x']+(pr['w']         if '+w' in where else 0) \
                ,  pr['y']+(pr['h']         if '+h' in where else 0)
        x, y    = (pr['x']+dx, pr['y']+dy)  if where=='dxdy' else (x, y)
        pass;                  #log('(x, y), (dx, dy), pr={}',((x, y), (dx, dy), pr))
        prXY    = _os_scale('scale', {'x':x, 'y':y})
        x, y    = prXY['x'], prXY['y']
        pass;                  #log('x, y={}',(x, y))
        x, y    = app.dlg_proc(self.did, app.DLG_COORD_LOCAL_TO_SCREEN, index=x, index2=y)
        pass;                  #log('x, y={}',(x, y))
        
        return show_menu(mn_content, x, y, self, repro_to_file)
       #def show_menu

    def _gen_repro_code(self):
        # Repro-code with only API calls
        pass;                   log4fun=-1==-1  # Order log in the function
        rtf     = self.opts.get('gen_repro_to_file', False)
        if not rtf: return 
        rerpo_fn= tempfile.gettempdir()+os.sep+(rtf if isinstance(rtf, str) else 'repro_dlg_proc.py')
        print(f(r'exec(open(r"{}", encoding="UTF-8").read())', rerpo_fn))

        l       = '\n'
        cattrs  = [  ('type', 'tag', 'act')
                    ,('name', 'x', 'y', 'w', 'h', 'w_min', 'h_min', 'w_max', 'h_max', 'cap', 'hint', 'p')
                    ,('en', 'vis', 'focused', 'tab_stop', 'tab_order'
                     ,'props', 'ex0', 'ex1', 'ex2', 'ex3', 'ex4', 'ex5', 'ex6', 'ex7', 'ex8', 'ex9'
                     ,'sp_l', 'sp_r', 'sp_t', 'sp_b', 'sp_a', 'a_l', 'a_r', 'a_t', 'a_b', 'align')
                    ,('val', 'items', 'columns')
                    ,('tp', 'b', 'r', 'tid', 'a', 'aid', 'def_bttn')
                    ]
        fattrs  = [  ('x', 'y', 'w', 'h', 'cap', 'tag')
                    ,('resize', 'w_min', 'w_max', 'h_min', 'h_max', 'topmost', 'focused')
#                   ,('vis', 'keypreview')
                    ]
        def out_attrs(pr, attrs, out=''):
            pr          = pr.copy()
            out         += '{'+l
            afix        = ''
            for ats in attrs:
                apr     =   {k:pr.pop(k) for k in ats if k in pr}
                if apr:
                    out += afix + ', '.join(repr(k) + ':' + repr(apr[k]) for k in ats if k in apr)
                    afix= '\n,'
            apr =           {k:pr.pop(k) for k in pr.copy() if k[0:3]!='on_'}
            if apr:
                out     += afix + repr(apr).strip('{}') 
            for k in pr:
                out     += afix + f('"{}":(lambda idd,idc,data:print("{}"))', k, k)
            out         += '}'
            return out
        srp     =    ''
        srp    +=    'idd=dlg_proc(0, DLG_CREATE)'
        srp    +=l
        cids    = []
        for idC in range(app.dlg_proc(self.did, app.DLG_CTL_COUNT)):
            prC = _dlg_proc(self.did, app.DLG_CTL_PROP_GET, index=idC)
            cids+=[prC['name']]
            if ''==prC.get('hint', ''):                 prC.pop('hint', None)
            if ''==prC.get('tag', ''):                  prC.pop('tag', None)
            if ''==prC.get('cap', ''):                  prC.pop('cap', None)
            if ''==prC.get('items', None):              prC.pop('items')
            if prC.get('tab_stop', None):               prC.pop('tab_stop')
            if prC['type'] in ('label',):               prC.pop('tab_stop', None)
            if prC['type'] in ('bevel',):               (prC.pop('tab_stop', None)
                                                        ,prC.pop('tab_order', None))
            if prC['type'] not in ('listview'
                                  ,'checklistview'):    prC.pop('columns', None)
            if prC['type'] in ('label'
                              ,'bevel'
                              ,'button'):               prC.pop('val', None)
            if prC['type'] in ('button'):               prC.pop('act', None)
            if not prC.get('act', False):               prC.pop('act', None)
            if not prC.get('focused', False):           prC.pop('focused', None)
            if prC.get('vis', True):                    prC.pop('vis', None)
            if prC.get('en', True):                     prC.pop('en', None)
            name = prC['name']
            c_pr = self.ctrls[name].copy()
            c_pr = self._prepare_it_vl(c_pr, c_pr)
            prC.update({k:v for k,v in c_pr.items() if k not in ('callback','on','menu')})
            srp+=l+f('idc=dlg_proc(idd, DLG_CTL_ADD,"{}");dlg_proc(idd, DLG_CTL_PROP_SET, index=idc, prop={})'
                    , prC.pop('type', None), out_attrs(prC, cattrs))
            srp+=l
        prD     = _dlg_proc(self.did, app.DLG_PROP_GET)
        prD.update(self.form)
#       srp    +=l
        fid     = prD.get('fid', prD['focused'])
        if fid not in cids:
            prD.pop('focused')
        srp    +=l+f('dlg_proc(idd, DLG_PROP_SET, prop={})', out_attrs(prD, fattrs))
        srp    +=l+(f('dlg_proc(idd, DLG_CTL_FOCUS, name="{}")', fid) if fid in cids else '')
        srp    +=l+  'dlg_proc(idd, DLG_SHOW_MODAL)'
        srp    +=l+  'dlg_proc(idd, DLG_FREE)'
        open(rerpo_fn, 'w', encoding='UTF-8').write(srp)
       #def _gen_repro_code

   #class DlgAg

def show_menu(mn_content, x, y, ag=None, repro_to_file=None):
    """ mn_content      [{cap:'', tag:'', en:T, mark:''|'c'|'r', cmd:(lambda ag, tag:''), sub:[]}]
        x, y            Screen coords for menu top-left corner
        repro_to_file   File name (w/o path) to write reprocode with only menu_proc 
    """
    rfn     = tempfile.gettempdir()+os.sep+repro_to_file            if repro_to_file else None
    print(f(r'exec(open(r"{}", encoding="UTF-8").read())', rfn))    if rfn else 0
    repro   = lambda line,*args,mod='a':(
                open(rfn, mod).write(line.format(*args)+'\n')       if rfn else 0)
    repro('import  cudatext as app', mod='w')
    
    def da_mn_callbk(it):
        pass;                  #log('it[tag]={}',(it['tag']))
        u_callbk= it['cmd']
        upds    = u_callbk(ag, it.get('tag', ''))
        if not ag:      return 
        if upds is None:                                        # To hide/close
            app.dlg_proc(ag.did, app.DLG_HIDE)
            return
        if not upds:    return  # No changes
        return ag.update(upds)
       #def da_mn_callbk
            
    def fill_mn(mid_prn, its):
        for it in its:
            if it['cap']=='-':
                app.menu_proc(  mid_prn, app.MENU_ADD, caption='-')
                repro("app.menu_proc(m{},app.MENU_ADD, caption='-')", mid_prn)
                continue
            mid =(app.menu_proc(mid_prn, app.MENU_ADD, caption=it['cap'], command= lambda _it=it:da_mn_callbk(_it))     # _it=it solves lambda closure problem
                    if 'cmd' in it else 
                  app.menu_proc(mid_prn, app.MENU_ADD, caption=it['cap'])
                 )
            repro("m{}=app.menu_proc(m{},app.MENU_ADD, caption='{}')", mid, mid_prn, it['cap'])
            if it.get('key', ''):
                app.menu_proc(      mid, app.MENU_SET_HOTKEY            , command=it['key'])
                repro("app.menu_proc(m{},app.MENU_SET_HOTKEY            , command='{}')", mid, it['key'])
                
            if it.get('mark', '')[:1]=='c' or it.get('mark', '')[:1]=='r' or it.get('ch', False) or it.get('rd', False):
                app.menu_proc(      mid, app.MENU_SET_CHECKED           , command=True)
                repro("app.menu_proc(m{},app.MENU_SET_CHECKED           , command=True)", mid)
            if it.get('mark', '')[:1]=='r' or it.get('rd', False):
                app.menu_proc(      mid, app.MENU_SET_RADIOITEM         , command=True)
                repro("app.menu_proc(m{},app.MENU_SET_RADIOITEM         , command=True)", mid)
                
            if not it.get('en', True):
                app.menu_proc(      mid, app.MENU_SET_ENABLED           , command=False)
                repro("app.menu_proc(m{},app.MENU_SET_ENABLED           , command=False)", mid)
            if 'sub' in it:
                fill_mn(mid, it['sub'])
       #def fill_mn
        
    mid_top = app.menu_proc(    0,       app.MENU_CREATE)
    repro("m{}=app.menu_proc(0,          app.MENU_CREATE)", mid_top)
    fill_mn(mid_top, mn_content)
    app.menu_proc(              mid_top, app.MENU_SHOW                  , command=f('{},{}', x, y))
    repro("app.menu_proc(       m{},     app.MENU_SHOW                  , command='{},{}')", mid_top, x, y)
    return []
   #def show_menu

OLD_PREFIX_FOR_USER_JSON = 'dlg_wrapper_fit_va_for_'
NEW_PREFIX_FOR_USER_JSON = 'dlg_ag_va_tunning_'
ENV2FITS= {'win':
            {'check'      :-2
            ,'radio'      :-2
            ,'edit'       :-3
            ,'button'     :-4
            ,'combo_ro'   :-4
            ,'combo'      :-3
            ,'checkbutton':-5
            ,'linklabel'  : 0
            ,'spinedit'   :-3
            }
          ,'unity':
            {'check'      :-3
            ,'radio'      :-3
            ,'edit'       :-5
            ,'button'     :-4
            ,'combo_ro'   :-5
            ,'combo'      :-6
            ,'checkbutton':-4
            ,'linklabel'  : 0
            ,'spinedit'   :-6
            }
          ,'mac':
            {'check'      :-1
            ,'radio'      :-1
            ,'edit'       :-3
            ,'button'     :-3
            ,'combo_ro'   :-2
            ,'combo'      :-3
            ,'checkbutton':-2
            ,'linklabel'  : 0
            ,'spinedit'   : 0   ##??
            }
          }

_FIT_REDUCTIONS  = {
     'linklabel': 'label'
    ,'edit_pwd' : 'edit'
    }
_fit_top_by_env__cache    = {}
def _fit_top_by_env__clear():
    global _fit_top_by_env__cache
    _fit_top_by_env__cache= {}
def _fit_top_by_env(what_tp, base_tp='label'):
    """ Get "fitting" to add to top of first control to vertical align inside text with text into second control.
        The fittings rely to platform: win, unix(kde,gnome,...), mac
    """
    what_tp = _FIT_REDUCTIONS.get(what_tp, what_tp)
    base_tp = _FIT_REDUCTIONS.get(base_tp, base_tp)
    if what_tp==base_tp:
        return 0
    if (what_tp, base_tp) in _fit_top_by_env__cache:        # Ready?
        pass;                  #log('cached what_tp, base_tp={}',(what_tp, base_tp))
        return _fit_top_by_env__cache[(what_tp, base_tp)]
    # Calc or restore, save in cache
    env     = get_desktop_environment()
    pass;                      #env = 'mac'
    fit4lb  = ENV2FITS.get(env, ENV2FITS.get('win'))
    fit     = 0
    if base_tp=='label':
        fit = apx.get_opt(NEW_PREFIX_FOR_USER_JSON+what_tp  # Query new setting
            , apx.get_opt(OLD_PREFIX_FOR_USER_JSON+what_tp  # Use old setting if no new one
                         ,fit4lb.get(what_tp, 0)))          # defaulf
        pass;                   fit_o=fit
        fit = _os_scale(app.DLG_PROP_GET, {'y':fit})['y']
        pass;                  #log('what_tp,fit_o,fit,h={}',(what_tp,fit_o,fit,_get_gui_height(what_tp)))
    else:
        fit = _fit_top_by_env(what_tp) - _fit_top_by_env(base_tp)
    pass;                      #log('what_tp, base_tp, fit={}',(what_tp, base_tp, fit))
    return _fit_top_by_env__cache.setdefault((what_tp, base_tp), fit)   # Save in cache
   #def _fit_top_by_env


DLG_CTL_ADD_SET = 26
_DLG_PROC_I2S={
 0:'DLG_CREATE'
,1:'DLG_FREE'
,5:'DLG_SHOW_MODAL'
,6:'DLG_SHOW_NONMODAL'
,7:'DLG_HIDE'
,8:'DLG_FOCUS'
,9:'DLG_SCALE'
,10:'DLG_PROP_GET'
,11:'DLG_PROP_SET'
,12:'DLG_DOCK'
,13:'DLG_UNDOCK'
,20:'DLG_CTL_COUNT'
,21:'DLG_CTL_ADD'
,26:'DLG_CTL_ADD_SET'
,22:'DLG_CTL_PROP_GET'
,23:'DLG_CTL_PROP_SET'
,24:'DLG_CTL_DELETE'
,25:'DLG_CTL_DELETE_ALL'
,30:'DLG_CTL_FOCUS'
,31:'DLG_CTL_FIND'
,32:'DLG_CTL_HANDLE'
}
_SCALED_KEYS = ('x', 'y', 'w', 'h'
            ,  'w_min', 'w_max', 'h_min', 'h_max'
            ,  'sp_l', 'sp_r', 'sp_t', 'sp_b', 'sp_a'
            )
def _os_scale(id_action, prop=None, index=-1, index2=-1, name=''):
    pass;                      #return prop
    pass;                      #log('prop={}',({k:prop[k] for k in prop if k in ('x','y')}))
    ppi     = app.app_proc(app.PROC_GET_SYSTEM_PPI, '')
    if ppi==96:
        return prop
    scale   = ppi/96
    pass;                      #log('id_dialog, id_action,scale={}',(id_dialog, _DLG_PROC_I2S[id_action],scale))
    if False:pass
    elif id_action in (app.DLG_PROP_SET     , app.DLG_PROP_GET
                      ,app.DLG_CTL_PROP_SET , app.DLG_CTL_PROP_GET
                      ,'scale', 'unscale'):
        
        def scale_up(prop_dct):
            for k in _SCALED_KEYS:
                if k in prop_dct and '_ready_'+k not in prop_dct:
                    prop_dct[k]   =             round(prop_dct[k] * scale)      # Scale!
        
        def scale_dn(prop_dct):
            for k in _SCALED_KEYS:
                if k in prop_dct and '_ready_'+k not in prop_dct:
#               if k in prop_dct:
                    prop_dct[k]   =             round(prop_dct[k] / scale)      # UnScale!
#                   prop_dct[k]   =               int(prop_dct[k] / scale)      # UnScale!
        
#       pass;                   print('a={}, ?? pr={}'.format(_DLG_PROC_I2S[id_action], {k:prop[k] for k in prop if k in _SCALED_KEYS or k=='name'}))
        if False:pass
        elif id_action==app.DLG_PROP_SET:                   scale_up(prop)
        elif id_action==app.DLG_CTL_PROP_SET and -1!=index: scale_up(prop)
        elif id_action==app.DLG_CTL_PROP_SET and ''!=name:  scale_up(prop)
        elif id_action==app.DLG_PROP_GET:                   scale_dn(prop)
        elif id_action==app.DLG_CTL_PROP_GET and -1!=index: scale_dn(prop)
        elif id_action==app.DLG_CTL_PROP_GET and ''!=name:  scale_dn(prop)

        elif id_action==  'scale':                          scale_up(prop)
        elif id_action=='unscale':                          scale_dn(prop)
#       pass;                   print('a={}, ok pr={}'.format(_DLG_PROC_I2S[id_action], {k:prop[k] for k in prop if k in _SCALED_KEYS or k=='name'}))
    return prop
   #def _os_scale

_gui_height_cache= { 
    'button'            :0
  , 'label'             :0
  , 'linklabel'         :0
  , 'combo'             :0
  , 'combo_ro'          :0
  , 'edit'              :0
  , 'spinedit'          :0
  , 'check'             :0
  , 'radio'             :0
  , 'checkbutton'       :0
  , 'filter_listbox'    :0
  , 'filter_listview'   :0
# , 'scrollbar'         :0
  }
def _get_gui_height(ctrl_type):
    """ Return real OS-specific height of some control
             'button'
             'label' 'linklabel'
             'combo' 'combo_ro'
             'edit' 'spinedit'
             'check' 'radio' 'checkbutton'
             'filter_listbox' 'filter_listview'
             'scrollbar'
    """
    global _gui_height_cache
    if 0 == _gui_height_cache['button']:
        for tpc in _gui_height_cache:
            _gui_height_cache[tpc]   = app.app_proc(app.PROC_GET_GUI_HEIGHT, tpc)
        pass;                  #log('_gui_height_cache={}',(_gui_height_cache))
        idd=app.dlg_proc(         0,    app.DLG_CREATE)
        for tpc in _gui_height_cache:
            idc=app.dlg_proc(   idd,    app.DLG_CTL_ADD, tpc)
            if idc is None: raise ValueError('Unknown type='+tpc)
            pass;              #log('tpc,idc={}',(tpc,idc))
            prc = {'name':tpc, 'x':0, 'y':0, 'w':1, 'cap':tpc
                , 'h':_gui_height_cache[tpc]}
            if tpc in ('combo' 'combo_ro'):
                prc['items']='item0'
            app.dlg_proc(       idd,    app.DLG_CTL_PROP_SET, index=idc, prop=prc)
        app.dlg_proc(           idd,    app.DLG_PROP_SET, prop={'x':-1000, 'y':-1000, 'w':100, 'h':100})
        app.dlg_proc(           idd,    app.DLG_SHOW_NONMODAL)

        ppi     = app.app_proc(app.PROC_GET_SYSTEM_PPI, '')
        if ppi!=96:
            # Try to scale height of controls
            scale   = ppi/96
            for tpc in _gui_height_cache:
                prc     = app.dlg_proc( idd,    app.DLG_CTL_PROP_GET, name=tpc)
                sc_h    = round(prc['h'] * scale)
                app.dlg_proc( idd,    app.DLG_CTL_PROP_SET, name=tpc, prop=dict(h=sc_h))

        for tpc in _gui_height_cache:
            prc = app.dlg_proc( idd,    app.DLG_CTL_PROP_GET, name=tpc)
            pass;              #log('prc={}',(prc))
            _gui_height_cache[tpc]   = prc['h']
        app.dlg_proc(           idd,    app.DLG_FREE)
        pass;                  #log('_gui_height_cache={}',(_gui_height_cache))
    
    return _gui_height_cache.get(ctrl_type, app.app_proc(app.PROC_GET_GUI_HEIGHT, ctrl_type))
   #def get_gui_height

def _dlg_proc(id_dialog, id_action, prop='', index=-1, index2=-1, name=''):
    """ Wrapper on app.dlg_proc 
        1. To set/get dlg-props in scaled OS
        2. New command DLG_CTL_ADD_SET to set props of created ctrl
    """
    if id_action==app.DLG_SCALE:
        return
    pass;                       log4fun=-1== 1  # Order log in the function
    pass;                       log('id_a={}({}), ind,ind2,n={}, prop={}',id_action, _DLG_PROC_I2S[id_action], (index, index2, name), prop) if iflog(log4fun,_log4mod) else 0
    if id_action==DLG_CTL_ADD_SET:  # Join ADD and SET for a control
        ctl_ind = app.dlg_proc( id_dialog, app.DLG_CTL_ADD, name, -1, -1, '')       # type in name
        if ctl_ind is None: raise ValueError('Unknown type='+name)
        return _dlg_proc(id_dialog, app.DLG_CTL_PROP_SET, prop, ctl_ind, -1, '')

    scale_on_set    = id_action in (app.DLG_PROP_SET, app.DLG_CTL_PROP_SET)
    scale_on_get    = id_action in (app.DLG_PROP_GET, app.DLG_CTL_PROP_GET)

    if scale_on_set:    _os_scale(id_action, prop, index, index2, name)
    res = app.dlg_proc(id_dialog, id_action, prop, index, index2, name)
    if scale_on_get:    _os_scale(id_action, res,  index, index2, name)
    return res
   #def _dlg_proc

def _form_acts(act, fprs=None, did=None, key4store=None):
    """ Save/Restore pos of form """
    pass;                       log4fun=-1== 1  # Order log in the function
    pass;                       log('act, fprs, did={}',(act, fprs, did)) if iflog(log4fun,_log4mod) else 0

    def gen_form_key(prs):      # Gen key from form caption
        fm_cap  = prs['cap']
        fm_cap  = fm_cap[:fm_cap.rindex(' (')]      if ' (' in fm_cap else fm_cap
        fm_cap  = fm_cap[:fm_cap.rindex(' [')]      if ' [' in fm_cap else fm_cap
        return fm_cap
        
    fprs    = _dlg_proc(did, app.DLG_PROP_GET)  if act=='save' and did else fprs
    fm_key  = key4store if key4store else gen_form_key(fprs)
    pass;                       log('fm_key, fprs={}',(fm_key, fprs)) if iflog(log4fun,_log4mod) else 0
    if False:pass
    elif act=='move' and fprs:
        prev    = get_hist(fm_key)
        pass;                   log('prev={}',(prev)) if iflog(log4fun,_log4mod) else 0
        if not prev:    return fprs
        if not fprs.get('resize', False):
            prev.pop('w', None)
            prev.pop('h', None)
        fprs.update(prev)
        pass;                   log('!upd fprs={}',(fprs)) if iflog(log4fun,_log4mod) else 0
        return fprs
    elif act=='save' and did:
        set_hist(fm_key, {k:v for k,v in fprs.items() if k in ('x','y','w','h')})
   #def _form_acts

######################################
#NOTE: tuning_valigns
######################################
class Command:
    def tuning_valigns(self):dlg_tuning_valigns()
   #class Command:
def dlg_tuning_valigns():
    pass;                      #log('ok')
    rsp     = False #changed
    UP,DN   = '↑↑','↓↓'
    CTRLS   = ['check'
              ,'edit'
              ,'button'   
              ,'combo_ro' 
              ,'combo'    
              ,'checkbutton'
#             ,'linklabel'
              ,'spinedit'
              ,'radio'
              ]
    CTRLS_SP= {'_sp'+str(1+ic):nc for ic, nc in enumerate(CTRLS)}

    FITS_OLD= {sp:_fit_top_by_env(nc) for sp, nc in CTRLS_SP.items()}
    fits    = {sp:_fit_top_by_env(nc) for sp, nc in CTRLS_SP.items()}           # See up_dn
    hints   = {sp:nc+': '+str(FITS_OLD[sp])+' (old), '+str(fits[sp])+' (new)' 
                for sp, nc in CTRLS_SP.items()}                                 # See up_dn

    def save():
        nonlocal rsp
        scam        = app.app_proc(app.PROC_GET_KEYSTATE, '')
        if not scam:    # Save
            changed = False
            for sp, nc in CTRLS_SP.items():
                fit = fits[sp]
                if fit==_fit_top_by_env(nc): continue#for
                apx.set_opt(NEW_PREFIX_FOR_USER_JSON+nc, fit)
                changed = True
               #for
            _fit_top_by_env__clear()    if changed else 0
            rsp = True
            return None#hide
            
#       if scam=='c':   # Report
#           rpt = 'env:'+get_desktop_environment()
#           rpt+= c13 + c13.join(hints.values())
#           aid_r, *_t = dlg_wrapper(_('Report'), 230,310,
#                [dict(cid='rprt',tp='me'    ,t=5   ,l=5 ,h=200 ,w=220)
#                ,dict(           tp='labl'    ,t=215 ,l=5        ,w=220  ,cap=_('Send the report to the address'))
#                ,dict(cid='mail',tp='ed'    ,t=235 ,l=5        ,w=220)
#                ,dict(           tp='labl'    ,t=265 ,l=5        ,w=150  ,cap=_('or post it on'))
#                ,dict(cid='gith',tp='ln-lb' ,t=265 ,l=155      ,w=70   ,cap='GitHub',props='https://github.com/kvichans/cuda_fit_v_alignments/issues')
#                ,dict(cid='-'   ,tp='bttn'    ,t=280 ,l=205-80   ,w=80   ,cap=_('Close'))
#                ], dict(rprt=rpt
#                       ,mail='kvichans@gmail.com')
#                ,  focus_cid='rprt')
        return {}
       #def save

    def up_dn(ag, cid, sht):
        pass;                  #log('cid,sht={}',(cid,sht))
        sp          = '_sp'+cid[-1]
        fits[sp]    = fits[sp] + sht
        hints[sp]   = CTRLS_SP[sp]+': '+str(FITS_OLD[sp])+' (old), '+str(fits[sp])+' (new)'
        return {'ctrls':[(cid ,dict(y=ag.cattr(cid, 'y')+sht ,hint=hints[sp] ))]}
       #def up_dn

    save_h  = _('Apply the tunings to controls of all dialogs.'
              '\rCtrl+Click  - Show data to mail report.')
    sbleq   = ' ==============='
    seqeq   = '================='
    sbl44   = ' 4444444444444444'
    n4444   = 444444444
    sped_pr = f('0,{},1', n4444)
    cs      = CTRLS
    cnts    = [0
    ,('lb1' ,dict(tp='labl' ,y= 10              ,x=   5 ,w=110  ,cap=cs[0]+sbleq))
    ,('ch1' ,dict(tp='chck' ,y= 10+fits['_sp1'] ,x= 115 ,w=110  ,cap=seqeq      ,hint=hints['_sp1']             ))
    ,('up1' ,dict(tp='bttn' ,y= 10-3            ,x=-105 ,w= 50  ,cap=UP ,on=lambda cid,ag,d: up_dn(ag,'ch1',-1) ))
    ,('dn1' ,dict(tp='bttn' ,y= 10-3            ,x= -55 ,w= 50  ,cap=DN ,on=lambda cid,ag,d: up_dn(ag,'ch1', 1) ))
                
    ,('lb2' ,dict(tp='labl' ,y= 40              ,x=   5 ,w=110  ,cap=cs[1]+sbleq))
    ,('ed2' ,dict(tp='edit' ,y= 40+fits['_sp2'] ,x= 115 ,w=110                  ,hint=hints['_sp2']   ,val=seqeq))
    ,('up2' ,dict(tp='bttn' ,y= 40-3            ,x=-105 ,w= 50  ,cap=UP ,on=lambda cid,ag,d: up_dn(ag,'ed2',-1) ))
    ,('dn2' ,dict(tp='bttn' ,y= 40-3            ,x= -55 ,w= 50  ,cap=DN ,on=lambda cid,ag,d: up_dn(ag,'ed2', 1) ))
                
    ,('lb3' ,dict(tp='labl' ,y= 70              ,x=   5 ,w=110  ,cap=cs[2]+sbleq))
    ,('bt3' ,dict(tp='bttn' ,y= 70+fits['_sp3'] ,x= 115 ,w=110  ,cap=seqeq      ,hint=hints['_sp3']             ))
    ,('up3' ,dict(tp='bttn' ,y= 70-3            ,x=-105 ,w= 50  ,cap=UP ,on=lambda cid,ag,d: up_dn(ag,'bt3',-1) ))
    ,('dn3' ,dict(tp='bttn' ,y= 70-3            ,x= -55 ,w= 50  ,cap=DN ,on=lambda cid,ag,d: up_dn(ag,'bt3', 1) ))
                
    ,('lb4' ,dict(tp='labl' ,y=100              ,x=   5 ,w=110  ,cap=cs[3]+sbleq))
    ,('cbo4',dict(tp='cmbr' ,y=100+fits['_sp4'] ,x= 115 ,w=110  ,items=[seqeq]  ,hint=hints['_sp4']   ,val=0   ))
    ,('up4' ,dict(tp='bttn' ,y=100-3            ,x=-105 ,w= 50  ,cap=UP ,on=lambda cid,ag,d: up_dn(ag,'cbo4',-1)))
    ,('dn4' ,dict(tp='bttn' ,y=100-3            ,x= -55 ,w= 50  ,cap=DN ,on=lambda cid,ag,d: up_dn(ag,'cbo4', 1)))
                
    ,('lb5' ,dict(tp='labl' ,y=130              ,x=   5 ,w=110  ,cap=cs[4]+sbleq))
    ,('cb5' ,dict(tp='cmbx' ,y=130+fits['_sp5'] ,x= 115 ,w=110  ,items=[seqeq]  ,hint=hints['_sp5']   ,val=seqeq))
    ,('up5' ,dict(tp='bttn' ,y=130-3            ,x=-105 ,w= 50  ,cap=UP ,on=lambda cid,ag,d: up_dn(ag,'cb5',-1) ))
    ,('dn5' ,dict(tp='bttn' ,y=130-3            ,x= -55 ,w= 50  ,cap=DN ,on=lambda cid,ag,d: up_dn(ag,'cb5', 1) ))
                
    ,('lb6' ,dict(tp='labl' ,y=160              ,x=   5 ,w=110  ,cap=cs[5]+sbleq))
    ,('chb6',dict(tp='chbt' ,y=160+fits['_sp6'] ,x= 115 ,w=110  ,cap=seqeq[:10] ,hint=hints['_sp6']             ))
    ,('up6' ,dict(tp='bttn' ,y=160-3            ,x=-105 ,w= 50  ,cap=UP ,on=lambda cid,ag,d: up_dn(ag,'chb6',-1)))
    ,('dn6' ,dict(tp='bttn' ,y=160-3            ,x= -55 ,w= 50  ,cap=DN ,on=lambda cid,ag,d: up_dn(ag,'chb6', 1)))
                
    ,('lb7' ,dict(tp='labl' ,y=190              ,x=   5 ,w=110  ,cap=cs[6]+sbl44))
    ,('sp7' ,dict(tp='sped' ,y=190+fits['_sp7'] ,x= 115 ,w=110  ,props=sped_pr  ,hint=hints['_sp7']   ,val=n4444))
    ,('up7' ,dict(tp='bttn' ,y=190-3            ,x=-105 ,w= 50  ,cap=UP ,on=lambda cid,ag,d: up_dn(ag,'sp7',-1) ))
    ,('dn7' ,dict(tp='bttn' ,y=190-3            ,x= -55 ,w= 50  ,cap=DN ,on=lambda cid,ag,d: up_dn(ag,'sp7', 1) ))
                
    ,('lb8' ,dict(tp='labl' ,y=220              ,x=   5 ,w=110  ,cap=cs[7]+sbleq))
    ,('rd8' ,dict(tp='rdio' ,y=220+fits['_sp8'] ,x= 115 ,w=110  ,cap=seqeq      ,hint=hints['_sp8']             ))
    ,('up8' ,dict(tp='bttn' ,y=220-3            ,x=-105 ,w= 50  ,cap=UP ,on=lambda cid,ag,d: up_dn(ag,'rd8',-1) ))
    ,('dn8' ,dict(tp='bttn' ,y=220-3            ,x= -55 ,w= 50  ,cap=DN ,on=lambda cid,ag,d: up_dn(ag,'rd8', 1) ))
                
    ,('save',dict(tp='bttn' ,y=-30              ,x=-220 ,w=110  ,cap=_('&Save') ,on=lambda cid,ag,d:save() ,hint=save_h))
    ,('-'   ,dict(tp='bttn' ,y=-30              ,x=-105 ,w=100  ,cap=_('Cancel'),on=CB_HIDE ))
    ][1:]
    agent   = DlgAg(form=dict(
                        cap=_('Tuning text vertical alignment for control pairs')
                    ,   w=335, h=310-30)
                ,   ctrls=cnts 
                ,   fid = '-'
                ,   opts={
                        'negative_coords_reflect':True
#                   ,   'gen_repro_to_file':'repro_tuning_valigns.py'
                        }
            ).show()    #NOTE: dlg_valign
    return rsp
   #def tuning_valigns

if __name__ == '__main__' :
    # To start the tests run in Console
    #   exec(open(path_to_the_file, encoding="UTF-8").read())

    app.app_log(app.LOG_CONSOLE_CLEAR, 'm')
    print('Start all tests')
    if -2==-2:
        for smk in [smk for smk 
            in  sys.modules                             if 'cuda_kv_dlg.tests.test_dlg_ag' in smk]:
            del sys.modules[smk]        # Avoid old module 
        import                                              cuda_kv_dlg.tests.test_dlg_ag
        import unittest
        suite = unittest.TestLoader().loadTestsFromModule(  cuda_kv_dlg.tests.test_dlg_ag)
        unittest.TextTestRunner().run(suite)
        
    if -1== 1:
        print('Start test1: dlg: (label, edit, button), (tid, call, update, hide, on_exit)')
        print('Stop test1')
    print('Stop all tests')
'''
ToDo
[+][kv-kv][13feb19] Extract from cd_plug_lib.py
[+][kv-kv][13feb19] Set tests
[+][kv-kv][15feb19] Add proxy for all form events
[+][kv-kv][15feb19] Add more calc for ctrl position
[+][kv-kv][15feb19] ? Reorder params in fattrs ?
[ ][kv-kv][15feb19] ? Cancel form moving by opt ?
[+][kv-kv][15feb19] Allow r=-10 as <gap to right border> by opt
[ ][kv-kv][15feb19] Allow repro from any state
[+][kv-kv][18feb19] Anchors
[+][kv-kv][18feb19] Menu
[+][kv-kv][18feb19] dlg_valigns
[ ][kv-kv][24feb19] Test for live attr on_exit
[+][kv-kv][25feb19] Allow dict for ctrls values
[ ][kv-kv][25feb19] Test focused in fattr
[+][at-kv][06mar19] ag set first in all cb
[?][at-kv][06mar19] Use "return False" as "return None" in cb
[ ][at-kv][06mar19] Test for panel in panel
[+][at-kv][06mar19] def handle for control/form
[+][at-kv][06mar19] negative_xy_as_reflex -> negative_coords_reflect
[ ][at-kv][06mar19] nonmodal?
'''
