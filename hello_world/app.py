import json
import pandas as pd
import categorise
import lists

# import requests


def lambda_handler(event, context):
    """Sample pure Lambda function

    Parameters
    ----------
    event: dict, required
        API Gateway Lambda Proxy Input Format

        Event doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-input-format

    context: object, required
        Lambda Context runtime methods and attributes

        Context doc: https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html

    Returns
    ------
    API Gateway Lambda Proxy Output Format: dict

        Return doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html
    """

    # try:
    #     ip = requests.get("http://checkip.amazonaws.com/")
    # except requests.RequestException as e:
    #     # Send some context about this error to Lambda Logs
    #     print(e)

    #     raise e

    # extract the json of transactions
    transaction_json = json.loads(event["body"])["body"]

    # convert json to df
    df=pd.read_json(transaction_json, orient = 'index')

    # format date
    df["Date"] = pd.to_datetime(df['Date'])
    df["Date"] =  [d.replace(tzinfo=None) for d in df['Date']]
    df["Date"] = df['Date'].astype('datetime64[ns]')

    # pass df to categorise function
    out_df, desc_groups_df, fuzzy_groups_df = categorise.categorise(df)

    # convert back to json
    out_json = out_df.to_json(orient = 'index')
    desc_groups_json = desc_groups_df.to_json(orient = 'index')
    fuzzy_groups_json = fuzzy_groups_df.to_json(orient = 'index')


    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "hello world",
            "event_body": str(transaction_json),
            "lists.salary_inc_lst": str(lists.salary_inc_lst),
            "shape_df": str(df.shape),
            "out_cats": str(out_json),
            "desc_groups": str(desc_groups_json),
            "fuzzy_groups": str(fuzzy_groups_json)

        }),
    }

    # return event

