def import_model(model_path: str, **kwargs):
    model_path, model_name = model_path.rsplit('.', 1)

    model = getattr(__import__(model_path, fromlist=[model_name]), model_name)
    instance = model(**kwargs)

    return instance
