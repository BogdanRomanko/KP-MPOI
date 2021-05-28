% Функция добавления нашей библиотеки в менеджер
% библиотек и регистрации её там на сеанс
function blkStruct = KP_lib
    % 'KP' это имя нашей библиотеки
	Browser.Library = 'KP';
	
	% 'KP Lib' это имя библиотеки
    % какое будет отображаться в менеджере библиотек
    Browser.Name = 'KP Lib';

    blkStruct.Browser = Browser;