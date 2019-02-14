### Пример 1.
Цели: 
- Отредактировать строку,
- Перестановка фокуса
- Выравнивание подписи и редактора
- Изменение надписи и перемещение для кнопки 

Контролы: `label`, `edit`, `button`

Демострирует: `tid`, `>`, `def_bttn`, `call`, `update`, `on_exit`, `cattr`, `cval`, `fid`
```python
    def test_1_dlg_ag(self):
        val4edit    = 'Edit me'
        print('val4edit=',val4edit)
        def do_call(cid, ag, data=''):
            if cid=='b1':
                return    dict(ctrls=[('b1', dict(cap='Renamed'))]
                              ,fid='b2')
            if cid=='b2':
                x = ag.cattr('b2', 'x')
                w = ag.cattr('b2', 'w')
                ag.update(dict(ctrls=[('b2', dict(x=x+20, w=w-40))]
                              ,fid='b3'))
                return []
            if cid=='b3':
                app.msg_box('Ask something', app.MB_OKCANCEL)
                return None # Close dlg
            return []
        def do_exit(ag):
            nonlocal val4edit
            val4edit = ag.cval('e1')
        DlgAg(
            ctrls=[0
   ,('b1',dict(tp='bttn',cap='Re&name me' ,x=0  ,y=  0      ,w=200  ,call=do_call))
   ,('l1',dict(tp='labl',cap='>he&re'     ,x=0  ,tid='e1'   ,w= 50))
   ,('e1',dict(tp='edit',val=val4edit     ,x=50 ,t= 30      ,w=150))
   ,('b2',dict(tp='bttn',cap='Sh&ort me'  ,x=0  ,y= 60      ,w=200  ,call=do_call))
   ,('b3',dict(tp='bttn',cap='A&sk,Close' ,x=0  ,y= 90      ,w=200  ,call=do_call))
   ,('cl',dict(tp='bttn',cap='Close'      ,x=0  ,y=120      ,w=200  ,call=CB_HIDE   ,def_bttn=1))
   ][1:]
        ,   form=dict(cap='Try1'                  ,h=150,w=200)
        ,   fid='e1'
        ).show(do_exit)
        print('val4edit=',val4edit)
```
![default](https://user-images.githubusercontent.com/7419630/52783796-0d544480-3064-11e9-8e13-3d482743f784.png)

Пояснения
1. Фокус на редактор при запуске диалога: `fid='e1'` в конструкторе DlgAg.
2. *Кнопка по умолчанию*: `def_bttn=1` при перечислении контролов.
3. Автоматическое выравнивание подписи `here` и строки `Edit me`: 
   - у редактора `e1` вместо `y` задан атрибут `t`,
   - у подписи `l1` вместо `y` задан атрибут `tid`, который указывает на `e1`.
4. Перехват события: `call` для кнопки вместо `on_change`.
5. Два способа обновить диалог при реакции на событие:
   - (`cid=='b2'`) вызывать `ag.update` с описанием изменений,
   - (`cid=='b1'`) вернуть описания изменений (такие же как при вызове `ag.update`).

### Пример 2
Цели: перевод кода *с оберткой* в код состоящий только из вызовов API.

Вызов такого кода

```python
    def test_ag_repro(self):
        # Tricks: repro code
        DlgAg(
            ctrls=[0
   ,('b1',dict(tp='bttn',cap='Re&name me' ,x=0  ,y=  0      ,w=200))
   ,('l1',dict(tp='labl',cap='>he&re'     ,x=0  ,tid='e1'   ,w= 50))
   ,('e1',dict(tp='edit',val='Edit me'    ,x=50 ,t= 30      ,w=150))
   ,('b2',dict(tp='bttn',cap='Sh&ort me'  ,x=0  ,y= 60      ,w=200))
   ,('b3',dict(tp='bttn',cap='A&sk,Close' ,x=0  ,y= 90      ,w=200))
   ,('cl',dict(tp='bttn',cap='Close'      ,x=0  ,y=120      ,w=200,def_bttn=1))
   ][1:]
        ,form=dict(cap='Demo "repro-code"'   ,h=150      ,w=200)
        ,fid='e1'    # Start focus
        ,opts=dict(gen_repro_to_file='repro_ag.py')
        ).show()
```

показывает 

![default](https://user-images.githubusercontent.com/7419630/52785262-98cfd480-3068-11e9-9731-3073931fe080.png)

и создает файл `<tempdir>/repro_ag.py` 

```python
idd=dlg_proc(0, DLG_CREATE)

idc=dlg_proc(idd, DLG_CTL_ADD,"button");dlg_proc(idd, DLG_CTL_PROP_SET, index=idc, prop={
'name':'b1'
,'x':0, 'y':0, 'w':200, 'h':25, 'cap':'Re&name me'
,'tab_order':0, 'sp_l':0, 'sp_r':0, 'sp_t':0, 'sp_b':0, 'sp_a':0
,'tp':'bttn'})

idc=dlg_proc(idd, DLG_CTL_ADD,"label");dlg_proc(idd, DLG_CTL_PROP_SET, index=idc, prop={
'name':'l1'
,'x':0, 'y':33, 'w':50, 'h':17, 'cap':'he&re'
,'tab_order':-1, 'ex0':True, 'sp_l':0, 'sp_r':0, 'sp_t':0, 'sp_b':0, 'sp_a':0
,'tp':'labl', 'tid':'e1'})

idc=dlg_proc(idd, DLG_CTL_ADD,"edit");dlg_proc(idd, DLG_CTL_PROP_SET, index=idc, prop={
'name':'e1'
,'x':50, 'y':30, 'w':150, 'h':25, 'cap':'Edit me'
,'tab_order':1, 'sp_l':0, 'sp_r':0, 'sp_t':0, 'sp_b':0, 'sp_a':0
,'val':'Edit me'
,'tp':'edit', 't':30})

idc=dlg_proc(idd, DLG_CTL_ADD,"button");dlg_proc(idd, DLG_CTL_PROP_SET, index=idc, prop={
'name':'b2'
,'x':0, 'y':60, 'w':200, 'h':25, 'cap':'Sh&ort me'
,'tab_order':2, 'sp_l':0, 'sp_r':0, 'sp_t':0, 'sp_b':0, 'sp_a':0
,'tp':'bttn'})

idc=dlg_proc(idd, DLG_CTL_ADD,"button");dlg_proc(idd, DLG_CTL_PROP_SET, index=idc, prop={
'name':'b3'
,'x':0, 'y':90, 'w':200, 'h':25, 'cap':'A&sk,Close'
,'tab_order':3, 'sp_l':0, 'sp_r':0, 'sp_t':0, 'sp_b':0, 'sp_a':0
,'tp':'bttn'})

idc=dlg_proc(idd, DLG_CTL_ADD,"button");dlg_proc(idd, DLG_CTL_PROP_SET, index=idc, prop={
'name':'cl'
,'x':0, 'y':120, 'w':200, 'h':25, 'cap':'Close'
,'tab_order':4, 'ex0':True, 'sp_l':0, 'sp_r':0, 'sp_t':0, 'sp_b':0, 'sp_a':0
,'tp':'bttn'
,'def_bttn': 1})

dlg_proc(idd, DLG_PROP_SET, prop={
'x':0, 'y':0, 'w':221, 'h':166, 'cap':'Demo "repro-code"', 'tag':''
,'resize':False
,'vis':False, 'keypreview':True
,'clicked': -1, 'topmost': True, 'fid': 'e1'})

dlg_proc(idd, DLG_SHOW_MODAL)
dlg_proc(idd, DLG_FREE)
```

Если запустить этот код, то появится 

![default](https://user-images.githubusercontent.com/7419630/52785332-c288fb80-3068-11e9-98e4-ee09a4e39a20.png)

Пояснения
1. Чтобы создать репро-код не обязательно показывать диалог - достаточно создать объект

`DlgAg(ctrls=[...], form={...}, fid='...', opts={'gen_repro_to_file':'repro_ag.py'))`
