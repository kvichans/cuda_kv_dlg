# cuda_kv_dlg
Wrapper for dlg_proc and more tools for plugin dialog 

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
   ,('b1', dict(tp='bttn'   ,cap='Re&name me'   ,x=0   ,y=  0      ,w=200  ,call=do_call))
   ,('l1', dict(tp='labl'   ,cap='>l&abel'      ,x=0   ,tid='e1'   ,w= 50))
   ,('e1', dict(tp='edit'   ,val=val4edit       ,x=50  ,t= 30      ,w=150))
   ,('b2', dict(tp='bttn'   ,cap='Sh&ort me'    ,x=0   ,y= 60      ,w=200  ,call=do_call))
   ,('b3', dict(tp='bttn'   ,cap='A&sk,Close'   ,x=0   ,y= 90      ,w=200  ,call=do_call))
   ,('cl', dict(tp='bttn'   ,cap='Close'        ,x=0   ,y=120      ,w=200  ,call=CB_HIDE   ,def_bttn=1))
   ][1:]
        ,   form=dict(cap='Try1'                  ,h=150,w=200)
        ,   fid='e1'
        ).show(do_exit)
        print('val4edit=',val4edit)
```
![default](https://user-images.githubusercontent.com/7419630/52783094-d9781f80-3061-11e9-8b9a-8009f675a19c.png)

Пояснения
1. Фокус на редактор при запуске диалога: `fid='e1'` в конструкторе DlgAg.
2. *Кнопка по умолчанию*: `def_bttn=1` при перечислении контролов.
