<h1 align="center">ScreenKeyboard</h1>
<h2 align="center">

[![Mentioned in Awesome Vue.js](https://awesome.re/mentioned-badge.svg)](https://github.com/vuejs/awesome-vue)

</h2>

<p align="center">
  
<img src="https://img.shields.io/npm/dy/silentlad">
<img src="https://img.shields.io/github/issues/ird87/ScreenKeyboard">
<img src="https://img.shields.io/github/forks/ird87/ScreenKeyboard">
<img src="https://img.shields.io/github/stars/ird87/ScreenKeyboard">
<img src="https://img.shields.io/github/license/ird87/ScreenKeyboard">

</p>

<img src="./readme_assets/h2.png" width="100%">

## Description

<p align="center">
<img src="./readme_assets/Keyboard.gif" width="100%"></p>

Экранная клавиатура была разработана для raspberry pi 3 с сенсорным экраном 480х320. 
По-умолчанию, она соответсвует этому размеру и отображается в верхнем левом углу экрана с некоторыми отступами;
Содержит однострочное поле для ввода и два языка: русский и английский, 
а так же цифровую клавиатуру в каждом из них.
Впрочем она полностью настраиваемая:

## Как использовать

```
from ScreenKeyboard import run
string result = run(settings={})

```
Клавиатура закрывается по клику вне ее пределов и возвращает пустое значение.
При подтверждении ввода возвращает введенный текст в качестве переменной str

## Настройка

### Размеры и положение

Размеры и положения по-умолчанию можно изменить/задать в файлах разметки клавиатуры для каждого языка:

```
<ScreenKeyboard width="480" locationX="0" locationY="0" languare="EN">
...
<EntryField height="30">
...
<InputBlock height = "120">
...
<GeneralButtons height = "40">
...
```

Или передать при вызове:

```
string result = run(settings={
    "w"  : 640, 
    "h1" : 40,  // EntryField height
    "h2" : 180, // InputBlock height
    "h3" : 60,  // GeneralButtons height
    "lx" : 100, 
    "ly" : 100
    })

```

### Добавить, удалить, изменить языки:

```
string result = run(settings={
    "languages_path" : os.path.join(os.path.dirname(os.path.realpath(__file__)), "languages"),
    })

```

- Укажите путь к папке с файлами разметки разных языков клавиатуры
- Поместите в эту папку файл(ы) с необходимыми разметками
- Клавиатура автоматически подхватывает все файлы из этой папки и последовательно переключает их

#### Правила разметки 
- Ширина указывается общая.
- Высота указывается для каждого из 3 блоков контролей своя
- в каждом блоке может быть **x** строк высотой **h/x**
- ширина каждого элемента задается через параметр **size** и рассчитывается 
как **width/12*size**, округление до ширины клавиатуры происходит за счет последнего элемента.
- field может быть только 1 - однострочный или многострочный.
- buttons могуты быть нескольких типов: 
  - **apply** - закрывает клавиатуру и возвращает введенный текст. Может быть с иконкой **icon** или подписью **text**. 
  - **input** - ввод сивола **value1** или **value2** в зависимости от того включен ли **shift**
  - **turn** - переключение режимов, имеет параметр **turnTarget**, который может быть *uppercase* или *numbers*
    Может быть с иконкой **iconTurnOn**/**iconTurnOff** или подписью **textTurnOn**/**textTurnOff**. 
  - **languare** - переключает все добавленные языки. Отображает название текущего.
  - **action** - выполняет действие, имеет параметр **action**, который может быть *backspace* или *enter*.
    Может быть с иконкой **icon** или подписью **text**. 

### Поле ввода

По-умолчанию задано в файле разметки

```
<field type="line" size="11.0"></field>
```

Можно изменить при вызове

```
string result = run(settings={
    "multiline" : True, 
    })

```

### Размер шрифта

В файле разметки:

```
<Font name="Helvetica" small="10" normal="16" large="20"></Font>
```

При вызове из программы:

```
string result = run(settings={
    "font" : 'Helvetica', 
    "font_size" : {
        "small" : 10,
        "normal" : 12,
        "large" : 14,
        }, 
    })

```

В разметке для каждого элемента можно указать **font-size** ("small", "normal", "large") 
и положение **align** ("top", "center", "bottom"). Если не указано: "normal" + "center"

### Путь к файлу с иконками для кнопок

```
"icon_path" : os.path.join(os.path.dirname(os.path.realpath(__file__)), "attachments"),  
```

### Настройка цветов кнопок

Только при вызове из программы:

```
string result = run(settings={
    "b_foreground_!active":"#ffffff", 
    "b_foreground_pressed":"#ffffff",
    "b_foreground_active":"#ffffff",
    "b_background_!active":"#232526",
    "b_background_pressed":"#484a4b",
    "b_background_active":"#484a4b",
    })

```

**Стандартный вид**

<p align="center">
<img src="./readme_assets/02.png" width="100%"></p>

**С отключенной настройкой цветов**

```
string result = run(settings={
    "b_customize":False, 
    })

```

<p align="center">
<img src="./readme_assets/01.png" width="100%"></p>