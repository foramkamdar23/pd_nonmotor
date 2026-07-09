addpath('C:\Users\cns-co-admin\Desktop\fk\repos\neurotoolbox\matlab\startup');
add_toolbox_paths;

%03062026
cfg = cfg_emoreg_defaults();

%CHANGE if needed 
cfg.task.manifestCsv = 'C:\Users\cns-co-admin\Desktop\fk\repos\pd_nonmotor\stimuli\blocks\pdnm091_sessions\PDNM091_practice_block_8.csv';
cfg.block     = 1;

% ===== SUBJECT =====
cfg.subject   = 'PDNM091';
cfg.session   = 4;
cfg.condition = 4;


% ===== SELECT TRIGGER SYSTEM =====
cfg.trig.system = 'brainproducts';   % 'biosemi' OR 'brainproducts'
cfg.trig.portName = 'COM7';        % Confij6789430011233556788jjfrm in Device Manager
cfg.trig.baud = 2000000;           % REQUIRED for TriggerBox Plus
cfg.trig.useTriggers = true;
cfg.trig.allowDummy  = ~cfg.trig.useTriggers;

% ===== PATHS =====
cfg.paths.imagesDir  = 'C:\Users\cns-co-admin\Desktop\fk\repos\Images\NAPS_H';
cfg.paths.scalesDir  = 'C:\Users\cns-co-admin\Desktop\fk\repos\neurotoolbox\SAM-Scales';
cfg.paths.resultsDir = 'C:\Users\cns-co-admin\Desktop\fk\repos\neurotoolbox\outputs';
cfg.paths.assetsDir  = 'C:\Users\cns-co-admin\Desktop\fk\repos\neurotoolbox\assets';


% ===== Eyelink =====
cfg.el.useEyelink    = true;


% ===== Millikey =====
cfg.keys.useNumpad = true;

% ===== Screen =====
cfg.screen.screenNumber = 2;

% ===== LOAD MANIFEST =====
manifest = readtable(cfg.task.manifestCsv);

% Photodiode
cfg.photo.sizePx = 50;
cfg.photo.marginPx = 10;
cfg.photo.pulseFrames = 2;

% ===== RUN TASK =====
Results = task_emoreg_run(cfg);