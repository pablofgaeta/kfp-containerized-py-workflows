from kfp import dsl

def component(
    n: int, sample_dataset: dsl.Output[dsl.Dataset], sample_metrics: dsl.Output[dsl.Metrics]
):
    import pandas as pd
    from user import stats

    sample = stats.gen_sample(n)

    # Write dataset to Output Dataset parquet file
    sample_df = pd.DataFrame({'sample': sample})
    sample_df.to_parquet(sample_dataset.path, engine='fastparquet')

    # Log mean to Metric Artifact
    mean = stats.sample_mean(sample)
    sample_metrics.log_metric("mean", mean)
