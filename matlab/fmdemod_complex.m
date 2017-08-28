function [m,t] = fmdemod_complex(y,fs,fc,fmdev)
%FMDEMOD Frequency demodulation of complex IQ baseband.

if ~isvector(y)
    error('I expect a complex vector y of IQ samples with FM carrier at f=0')
end

y = y(:);

t =(0:length(y)-1)/fs;
%% freq shift if necessary
if ~isempty(fc)
    y = y .* exp(-1j*2*pi*fc*t).';
    disp(['used carrier offset [Hz]',num2str(fc)])
end
%% fm demodulation
m = fs/(2*pi*fmdev) * [0; diff(unwrap(angle(y)))];
end