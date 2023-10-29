from kfp.dsl import Output, Dataset, Metrics

def component(
    config: dict, sample_dataset: Output[Dataset], mean_value: Output[Metrics]
):
    import pandas as pd
    from user.utils import stats

    n = config["n"]
    sample = stats.gen_sample(n)

    # Write dataset to Output Dataset parquet file
    sample_df = pd.DataFrame({'sample': sample})
    sample_df.to_parquet(sample_dataset.path, engine='fastparquet')

    # Log mean to Metric Artifact
    mean = stats.sample_mean(sample)
    mean_value.log_metric("mean", mean)
