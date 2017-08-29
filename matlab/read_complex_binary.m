% https://github.com/gnuradio/gnuradio/blob/master/gr-utils/octave/read_complex_binary.m
%
% Copyright 2001 Free Software Foundation, Inc.
% improved by Michael Hirsch, Ph.D.

function v = read_complex_binary (filename, count,start)
% data = read_complex_binary (filename, [count])
%
%  open filename and return the contents as a column vector,
%  treating them as 32 bit complex numbers
Lbyte = 8;  % complex64 data

 narginchk (1,3)
 
  if nargin < 2 || isempty(count)
    count = Inf;
  end
  if nargin < 3 || isempty(start)
    start = [];
  end

  f = fopen(filename, 'rb');
  if (f < 0)
    error([filename,' not found'])
  else
    if ~isempty(start)
        fseek(f,(start-1)*Lbyte,'bof');
    end
    v = fread (f, [2, count], 'float32=>float32');
    fclose (f);
    % have to be column major or Matlab will be horribly slow.
    v = (v(1,:) + v(2,:)*1i); 
    v = v(:);
  end