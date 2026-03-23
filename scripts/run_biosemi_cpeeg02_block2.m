addpath('C:\Users\cns-co-admin\Desktop\fk\repos\neurotoolbox\matlab\startup');
add_toolbox_paths;

%03062026
cfg = cfg_emoreg_defaults();

% ===== SELECT TRIGGER SYSTEM =====
cfg.trig.system = 'biosemi';
cfg.trig.port   = 'COM7';      % (was portName)
cfg.trig.baud   = 115200;      % (was baudRate; set to what worked before)
cfg.trig.lowVal = 0;
cfg.trig.pulseWidth = 0.005;


% ===== SUBJECT =====
cfg.subject   = 'CPEEG01';
cfg.session   = 1;
cfg.condition = 1;
cfg.block     = 1;

% ===== PATHS =====
cfg.paths.imagesDir  = 'C:\Users\cns-co-admin\Desktop\fk\repos\Images\NAPS_H';
cfg.paths.scalesDir  = 'C:\Users\cns-co-admin\Desktop\fk\repos\neurotoolbox\SAM-Scales';
cfg.paths.resultsDir = 'C:\Users\cns-co-admin\Desktop\fk\repos\neurotoolbox\outputs';
cfg.paths.assetsDir  = 'C:\Users\cns-co-admin\Desktop\fk\repos\neurotoolbox\assets';

%cfg.task.manifestCsv = 'C:\Users\cns-co-admin\Desktop\fk\repos\cp_nonmotor\stimuli\blocks\pilot_block_1.csv';
cfg.task.manifestCsv = 'C:\Users\cns-co-admin\Desktop\fk\repos\cp_nonmotor\stimuli\blocks\cpeeg01_block_96.csv';

% ===== Eyelink =====clcclccc
cfg.el.useEyelink    = true;


% ===== Millikey =====
cfg.keys.useNumpad = true;

% ===== Screen =====
cfg.screen.screenNumber = 2;

% ===== LOAD MANIFEST =====
manifest = readtable(cfg.task.manifestCsv);

% Photodiode
cfg.photo.sizePx = 90;
cfg.photo.marginPx = 10;
cfg.photo.pulseFrames = 2;

% ===== RUN TASK =====
Results = task_emoreg_run(cfg);