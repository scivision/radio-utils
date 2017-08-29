function [y,t] = amdemod_complex(y, fs, fc)
%AMDEMOD Amplitude demodulation of complex IQ baseband.

if ~isvector(y)
    error('I expect a complex vector y of IQ samples with FM carrier at f=0')
end

y = y(:);

t =(0:length(y)-1)/fs;
%% freq shift if necessary
if ~isempty(fc)
    y = y .* exp(-1j*2*pi*fc*t).';    
end % if

%y = filtfilt(b, 1, y); % channel filter (keep out adjacent stations, optional)
y = real(y.*2); % ideal diode

end % function