import sqlite3


class PostParser:
    def __init__(self, headers, num_epochs=None):
        self.name = headers.get('dev_name')
        self.model_name = headers.get('model_name')
        self.columns = ('name', 'model', 'epoch', 'val_loss', 'val_accuracy', 'loss', 'accuracy')
        if num_epochs:
            self.num_epochs = headers.get('num_epochs')
        self.conn = sqlite3.connect(r"C:\Users\79161\PycharmProjects\RemoteML\models.db")
        self.cursor = self.conn.cursor()

    def save_model_info(self, message):
        stats = [self.name, self.model_name]
        for i in list(message.values()):
            stats.append(i)
        self.cursor.execute("""INSERT INTO model_without_full_2 VALUES """ + str((tuple(stats))))
        self.conn.commit()
        return

    def delete(self):
        self.cursor.execute("""DELETE FROM model_without_full_2 WHERE user = ? AND model = ?""",
                            (self.name, self.model_name))
        self.conn.commit()

    def full(self):  # debugging method
        full_hist = [row for row in
                     self.cursor.execute("""Select * From model_without_full_2""")]
        print('Full history:', full_hist)

    def reg(self, message):  # debugging method
        login = message['login']
        if self.cursor.execute("""Select * From model_without_full_2 Where user=""" + login):
            return {'result': 'already_exist'}
        else:
            return {'result': 'success'}


class GetParser:
    def __init__(self, arguments):
        self.name = arguments['name']
        self.model = arguments['model']
        self.target = arguments['target']

        self.conn = sqlite3.connect(r"C:\Users\79161\PycharmProjects\RemoteML\models.db")
        self.cursor = self.conn.cursor()

        self.columns = ('name', 'model', 'epoch', 'val_loss', 'val_accuracy', 'loss', 'accuracy')

    def all_by_name(self):
        try:
            full_hist = [row[1] for row in self.cursor.execute("""Select * From model_without_full_2 Where user="""
                                                           + self.name)]
        except Exception as ex:
            return 'no_such_user'
        print(full_hist)
        return full_hist

    # def all_by_model(self):
    #     full_hist = [row[1] for row in self.cursor.execute("""Select * From model_without_full_2 Where model=""" + self.model)]
    #     if len(full_hist) == 0:
    #         return 'no_such_model'
    #     else:
    #         print(full_hist)
    #         return full_hist

    def get_model(self):
        try:
            full_hist = [row for row in self.cursor.execute("""Select * From model_without_full_2 Where user=""" +
                                                            self.name + """model=""" + self.model)]
        except Exception as ex:
            return 'no_such_model'
        print(full_hist[-1])
        return full_hist[-1]

    def run(self):
        if self.target == 'all_by_name':
            return self.all_by_name()
        # elif self.target == 'all_by_model':
        #     return self.all_by_model()
        elif self.target == 'exact':
            return self.get_model()
        else:
            return 'no_such_target'
