from app import db

# Tabla intermedia para la relación muchos a muchos
especialidad_plan = db.Table('especialidad_plan',
    db.Column('especialidad_id', db.Integer, db.ForeignKey('especialidades.id'), primary_key=True),
    db.Column('plan_id', db.Integer, db.ForeignKey('planes.id'), primary_key=True)
)

class Plan(db.Model):
    __tablename__ = 'planes'
    
    id = db.Column(db.Integer, primary_key=True)
    plan = db.Column(db.String(10), nullable=False)
    nombre = db.Column(db.String(255), nullable=False)
    
    # Relación muchos a muchos con especialidades
    especialidades = db.relationship('EspecialidadModel', 
                                   secondary=especialidad_plan,
                                   backref=db.backref('planes', lazy='dynamic'))