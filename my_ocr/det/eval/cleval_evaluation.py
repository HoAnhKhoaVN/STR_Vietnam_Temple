from cleval import CLEvalMetric
import json

if __name__ == '__main__':
    metric = CLEvalMetric()

    # region get gt

    # endregion


    # region get predictions:


    # endregion

    # region 

    for gt, det in zip(gts, dets):
        # your fancy algorithm
        # ...
        # gt_quads = ...
        # det_quads = ...
        # ...
        _ = metric(det_quads, gt_quads, det_letters, gt_letters, gt_is_dcs)

    metric_out = metric.compute()
    metric.reset()