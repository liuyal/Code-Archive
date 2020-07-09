function varargout = SGUi(varargin)
% SGUI MATLAB code for SGUi.fig
%      SGUI, by itself, creates a new SGUI or raises the existing
%      singleton*.
%      H = SGUI returns the handle to a new SGUI or the handle to
%      the existing singleton*.
%
%      SGUI('CALLBACK',hObject,eventData,handles,...) calls the local
%      function named CALLBACK in SGUI.M with the given input arguments.
%
%      SGUI('Property','Value',...) creates a new SGUI or raises the
%      existing singleton*.  Starting from the left, property value pairs are
%      applied to the GUI before SGUi_OpeningFcn gets called.  An
%      unrecognized property name or invalid value makes property application
%      stop.  All inputs are passed to SGUi_OpeningFcn via varargin.
%
%      *See GUI Options on GUIDE's Tools menu.  Choose "GUI allows only one
%      instance to run (singleton)".
%
% See also: GUIDE, GUIDATA, GUIHANDLES
% Edit the above text to modify the response to help SGUi
% Last Modified by GUIDE v2.5 12-Dec-2016 12:39:45
% Begin initialization code - DO NOT EDIT

gui_Singleton = 1;
gui_State = struct('gui_Name',       mfilename, ...
    'gui_Singleton',  gui_Singleton, ...
    'gui_OpeningFcn', @SGUi_OpeningFcn, ...
    'gui_OutputFcn',  @SGUi_OutputFcn, ...
    'gui_LayoutFcn',  [] , ...
    'gui_Callback',   []);
if nargin && ischar(varargin{1})
    gui_State.gui_Callback = str2func(varargin{1});
end

if nargout
    [varargout{1:nargout}] = gui_mainfcn(gui_State, varargin{:});
else
    gui_mainfcn(gui_State, varargin{:});
end
% End initialization code - DO NOT EDIT


%////////////////////////////////// | //////////////////////////////////
% --- Executes just before SGUi is made visible.
function SGUi_OpeningFcn(hObject, eventdata, handles, varargin)

% handles.data = Open('C:\Users\LAEC\Desktop\GUI\Data');
handles.data = Open('Z:\Co-op Students\Jerry\Martin\GUI\Data');

data = handles.data;
for i = 1:length(data)
    names{i} = data{i}.FolderName;
end
set(handles.listbox2,'String',names)

set(handles.checkbox1,'Value',0)
set(handles.checkbox2,'Value',0)
set(handles.checkbox3,'Value',0)
set(handles.checkbox4,'Value',0)
set(handles.checkbox5,'Value',0)
set(handles.checkbox6,'Value',0)
set(handles.checkbox7,'Value',0)

set(handles.listbox4,'String',data{1}.FolderName)
set(handles.listbox2, 'Min', 0, 'Max', 2);
set(handles.text4, 'String', ['Current Data: ' data{1}.FolderName])
set(handles.text5, 'String', '[Parameter]');
set(handles.text7, 'String', 'Note: ');
set(handles.popupmenu1, 'String', {'Signature Curve', 'Ambient Zero', 'Thermal R'});

handles.plot_data{1} = data{1};
handles.current_data = data{1};
handles.panel = zeros(1,7);
handles.plot_option = struct('PlotMode',1,'MaxPlot',60, 'MinPlot',20,'PlotTick', 5 ,'ErrorBars', 0, 'SlopeUn', 0);
set(handles.edit1, 'String', '60');
set(handles.edit2, 'String', '20');
set(handles.edit3, 'String', '5');

handles.list2_select_data = [];
handles.list4_select_data = [];
handles.lastList2_index = [];

plot_Pan(hObject, eventdata, handles)

handles.output = hObject;
guidata(hObject, handles); % Update handles structure

% --- Outputs from this function are returned to the command line.
function varargout = SGUi_OutputFcn(hObject, eventdata, handles)
clc;
datetime('now')
disp (['   Number of Data: ' num2str(length(handles.data))])
% Get default command line output from handles structure
varargout{1} = handles.output;
%////////////////////////////////// | //////////////////////////////////


% **************************** Open ****************************
% --- Executes on button press in pushbutton1.
function pushbutton1_Callback(hObject, eventdata, handles)
path = handles.current_data.Path;
path = char(['explorer ' path]);
dos(path);
guidata(hObject,handles);
% **************************** + ****************************
% --- Executes on button press in pushbutton2.
function pushbutton2_Callback(hObject, eventdata, handles)
% if isempty(handles.plot_data)
%     return;
% end
% selected = get(handles.listbox4,'Value');
% prev_str = get(handles.listbox4, 'String');
% if selected == 1
%     selected = 2;
% end
%
% if ~isempty(prev_str)
%     prev_str(get(handles.listbox4,'Value')) = [];
%
%     if length(handles.plot_data) == 1
%         set(handles.listbox4, 'String', ' ');
%     else
%         set(handles.listbox4, 'String', prev_str, ...
%             'Value', min(selected,length(prev_str)));
%     end
%     handles.current_data = handles.plot_data{selected-1};
%     handles.list4_select_data = handles.plot_data(selected-1);
%     if length(handles.plot_data) == 1
%         handles.plot_data(1) = [];
%         handles.current_data(1) = [];
%         set(handles.text4, 'String', ['Current Data: '])
%     else
%         handles.plot_data(selected) = [];
% %         set(handles.text4, 'String', ['Current Data: ' handles.current_data.FolderName])
%     end
% end
guidata(hObject,handles);
% handles    structure with handles and user data (see GUIDATA)


% **************************** Right List ****************************
% --- Executes on selection change in listbox2.
function listbox2_Callback(hObject, eventdata, handles)

index = handles.listbox2.Value;
handles.list2_select_data = handles.data(index);
handles.plot_data = handles.list2_select_data;

if ~isempty(index)
    for i = 1:length(handles.plot_data)
        names{i} = handles.plot_data{i}.FolderName;
    end
    set(handles.listbox4,'Value',length(index));
    set(handles.listbox4,'String',names)
elseif isempty(index)
    set(handles.listbox4,'String','')
end

if isempty(index)
else
    plot_Pan(hObject, eventdata, handles)
end

if isempty(index)
    set(handles.text4, 'String', 'Current Data: ')
    set(handles.text5, 'String', '[Parameter]');
    set(handles.text7, 'String', 'Note: ');
elseif length(names) == 1
    handles.current_data = handles.data{index};
    set(handles.text4, 'String', ['Current Data: ' handles.current_data.FolderName])
    txt = handles.current_data.Parameter;
    if ~isempty(txt)
        S = '';
        for i = 1:length(txt)-1
            A = strjoin(txt{i});
            S = char(S,A);
        end
        S(1,:) = [];
        S = char('[Parameter]',S);
        set(handles.text5, 'String', S)
        A = strjoin(txt{end});
        set(handles.text7, 'String', A);
    end
    
elseif length(names) > 1
    A = index;
    B = handles.lastList2_index;
    x = setdiff(A,B);
    if isempty(x) % Remove one select
        x = setdiff(B,A);
    end
    if isempty(x) % Remove one select
        return;
    end
    if length(x) > 1
        x = x(end);
    end
    handles.current_data = handles.data{x};
    set(handles.text4, 'String', ['Current Data: ' handles.current_data.FolderName]);
    txt = handles.current_data.Parameter;
    if ~isempty(txt)
        S = '';
        for i = 1:length(txt)-1
            A = strjoin(txt{i});
            S = char(S,A);
        end
        S(1,:) = [];
        S = char('[Parameter]',S);
        set(handles.text5, 'String', S)
        A = strjoin(txt{end});
        set(handles.text7, 'String', A);
    end
end
handles.lastList2_index = index;
guidata(hObject,handles);            %Update Data in handles
% --- Executes during object creation, after setting all properties.
function listbox2_CreateFcn(hObject, eventdata, handles)
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end

% **************************** Left List ****************************
% --- Executes on selection change in listbox4.
function listbox4_Callback(hObject, eventdata, handles)
index = handles.listbox4.Value;
if isempty(index)
    set(handles.text4, 'String', 'Current Data: ')
    set(handles.text5, 'String', '[Parameter]')
else
    handles.list4_select_data = handles.plot_data(index);
    handles.current_data = handles.plot_data{index};
    set(handles.text4, 'String', ['Current Data: ' handles.list4_select_data{1}.FolderName])
    txt = handles.list4_select_data{:}.Parameter;
    if ~isempty(txt)
        S = '';
        for i = 1:length(txt)-1
            A = strjoin(txt{i});
            S = char(S,A);
        end
        S(1,:) = [];
        S = char('[Parameter]',S);
        set(handles.text5, 'String', S)
        A = strjoin(txt{end});
        set(handles.text7, 'String', A);
    end
end
guidata(hObject,handles); %Update Data in handles
% --- Executes during object creation, after setting all properties.
function listbox4_CreateFcn(hObject, eventdata, handles)
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end% ************************************************************


% //////////////////////////// CheckBox /////////////////////////////////
% --- Executes on button press in checkbox1.
function checkbox1_Callback(hObject, eventdata, handles)
on = handles.checkbox1.Value;
handles.panel(1) = on;
plot_Pan(hObject, eventdata, handles);
guidata(hObject,handles);
% --- Executes on button press in checkbox2.
function checkbox2_Callback(hObject, eventdata, handles)
on = handles.checkbox2.Value;
handles.panel(2) = on;
plot_Pan(hObject, eventdata, handles);
guidata(hObject,handles);
% ---Executes on button press in checkbox3.
function checkbox3_Callback(hObject, eventdata, handles)
on = handles.checkbox3.Value;
handles.panel(3) = on;
plot_Pan(hObject, eventdata, handles);
guidata(hObject,handles);
% --- Executes on button press in checkbox4.
function checkbox4_Callback(hObject, eventdata, handles)
on = handles.checkbox4.Value;
handles.panel(4) = on;
plot_Pan(hObject, eventdata, handles);
guidata(hObject,handles);
% --- Executes on button press in checkbox5.
function checkbox5_Callback(hObject, eventdata, handles)
on = handles.checkbox5.Value;
handles.panel(5) = on;
plot_Pan(hObject, eventdata, handles);
guidata(hObject,handles);
% Hint: get(hObject,'Value') returns toggle state of checkbox5
% --- Executes on button press in checkbox6.
function checkbox6_Callback(hObject, eventdata, handles)
on = handles.checkbox6.Value;
handles.panel(6) = on;
plot_Pan(hObject, eventdata, handles);
guidata(hObject,handles);
% --- Executes on button press in checkbox7.
function checkbox7_Callback(hObject, eventdata, handles)
on = handles.checkbox7.Value;
handles.panel(7) = on;
plot_Pan(hObject, eventdata, handles);
guidata(hObject,handles);

% --- ERROR BARS *******************************************************
function checkbox9_Callback(hObject, eventdata, handles)
on = handles.checkbox9.Value;
handles.plot_option.ErrorBars = on;
plot_Pan(hObject, eventdata, handles);
guidata(hObject,handles);

% --- SlopeUN *******************************************************
function checkbox10_Callback(hObject, eventdata, handles)
on = handles.checkbox10.Value;
handles.plot_option.SlopeUn = on;
plot_Pan(hObject, eventdata, handles);
guidata(hObject,handles);
% ///////////////////////////// END CheckBox ///////////////////////////


%  **************************** MAX  ****************************
function edit1_Callback(hObject, eventdata, handles)
value = handles.edit1.String;
value = str2double(value);
handles.plot_option.MaxPlot = value;
plot_Pan(hObject, eventdata, handles);
guidata(hObject,handles);
% --- Executes during object creation, after setting all properties.
function edit1_CreateFcn(hObject, eventdata, handles)
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end
%  **************************** MIN  ****************************
function edit2_Callback(hObject, eventdata, handles)
value = handles.edit2.String;
value = str2double(value);
handles.plot_option.MinPlot = value;
plot_Pan(hObject, eventdata, handles);
guidata(hObject,handles);
% --- Executes during object creation, after setting all properties.
function edit2_CreateFcn(hObject, eventdata, handles)
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end
%  **************************** Ticks  ****************************
function edit3_Callback(hObject, eventdata, handles)
value = handles.edit3.String;
value = str2double(value);
max = handles.edit1.String;
max = str2double(max);
if value >= max || value <= 0
    set(handles.edit3, 'String', '5');
    handles.plot_option.PlotTick = 5;
    return;
end
handles.plot_option.PlotTick = value;
plot_Pan(hObject, eventdata, handles);
guidata(hObject,handles);
% --- Executes during object creation, after setting all properties.
function edit3_CreateFcn(hObject, eventdata, handles)
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end%//////////////////////////////////  //////////////////////////////////


%////////////////////////////////// Plot Mode //////////////////////////////////
function popupmenu1_Callback(hObject, eventdata, handles)
mode = get(handles.popupmenu1, 'Value');
handles.plot_option.PlotMode = mode;
if mode == 1;
    handles.plot_option.MaxPlot = 60;
    handles.plot_option.MinPlot = 20;
    handles.plot_option.PlotTick = 5;
    set(handles.edit1, 'String', '60');
    set(handles.edit2, 'String', '20');
    set(handles.edit3, 'String', '5');
elseif mode == 2;
    handles.plot_option.MaxPlot = 50;
    handles.plot_option.MinPlot = 0;
    handles.plot_option.PlotTick = 5;
    set(handles.edit1, 'String', '50');
    set(handles.edit2, 'String', '0');
    set(handles.edit3, 'String', '5');
elseif mode == 3;
    handles.plot_option.MaxPlot = 6;
    handles.plot_option.MinPlot = 0;
    handles.plot_option.PlotTick = 1;
    set(handles.edit1, 'String', '6');
    set(handles.edit2, 'String', '0');
    set(handles.edit3, 'String', '1');
end
plot_Pan(hObject, eventdata, handles);
guidata(hObject,handles);
% --- Executes during object creation, after setting all properties.
function popupmenu1_CreateFcn(hObject, eventdata, handles)
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end%//////////////////////////////////  //////////////////////////////////

%//////////////////////////////////  //////////////////////////////////
% --- Executes during object creation, after setting all properties.
function text4_CreateFcn(hObject, eventdata, handles)
% handles    empty - handles not created until after all CreateFcns called
