"""
"""

_base_ = [
    './seamamba.py'
]

ver = 'v26'
experiment_name = f'seamamba_uieb_{ver}'
work_dir = f'./work_dirs/{experiment_name}'
save_dir = './work_dirs/'

# model settings
model = dict(
    type='BaseEditModel',
    generator=dict(
        type='MM_VSSM',
        depths=[1]*6,
        dims=[48]*6,
        d_state=12,
        biattn_act_ratio=0.25,
        ver='v16',
    ),
    pixel_loss=dict(type='CharbonnierLoss'))

batch_size = 32
train_dataloader = dict(batch_size=batch_size)
val_dataloader = dict(batch_size=batch_size)

optim_wrapper = dict(
    dict(
        type='AmpOptimWrapper',
        optimizer=dict(type='AdamW', lr=0.0002, betas=(0.9, 0.999), weight_decay=0.5)))

max_epochs = 800
param_scheduler = [
    dict(
        type='LinearLR', start_factor=0.001, by_epoch=True, begin=0, end=15),
    dict(type='MultiStepLR', by_epoch=True, milestones=[50,200,400,600,700,720], gamma=0.5)]

train_cfg = dict(by_epoch=True, max_epochs=max_epochs)

visualizer = dict(
    vis_backends=[dict(type='LocalVisBackend'), dict(type='WandbVisBackend', init_kwargs=dict(project='seamamba', name=ver))])

auto_scale_lr = dict(enable=False)
default_hooks = dict(logger=dict(interval=5))

custom_hooks = [dict(type='BasicVisualizationHook', interval=4)]
