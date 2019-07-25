from math import sqrt
import sys
import math

from .framework import (Framework, Keys, main)
from Box2D import (b2CircleShape, b2FixtureDef,
                   b2PolygonShape, b2Random, b2EdgeShape, b2MassData)
from Box2D import (b2Vec2, b2_epsilon, b2BodyDef, b2ChainShape,
                   b2ParticleGroupDef, b2ParticleColor, b2RevoluteJointDef)

import Box2D


class WaveMachine (Framework):
    name = "WaveMachine Test"
    description = ''

    def __init__(self):
        super(WaveMachine, self).__init__()
        bd = b2BodyDef()
        ground = self.world.CreateBody(bd)

        bd = b2BodyDef()
        bd.type = Box2D.b2_dynamicBody
        bd.allowSleep = False
        bd.position.Set(0.0, 1.0)
        body = self.world.CreateBody(bd)

        shape = b2PolygonShape()
        shape.SetAsBox(0.05, 1.0, b2Vec2(2.0, 0.0), 0.0)
        body.CreateFixture(b2FixtureDef(shape=shape, density=5.0))
        shape.SetAsBox(0.05, 1.0, b2Vec2(-2.0, 0.0), 0.0)
        body.CreateFixture(b2FixtureDef(shape=shape, density=5.0))
        shape.SetAsBox(2.0, 0.05, b2Vec2(0.0, 1.0), 0.0)
        body.CreateFixture(b2FixtureDef(shape=shape, density=5.0))
        shape.SetAsBox(2.0, 0.05, b2Vec2(0.0, -1.0), 0.0)
        body.CreateFixture(b2FixtureDef(shape=shape, density=5.0))

        jd = b2RevoluteJointDef()
        jd.bodyA = ground
        jd.bodyB = body
        jd.localAnchorA.Set(0.0, 1.0)
        jd.localAnchorB.Set(0.0, 0.0)
        jd.referenceAngle = 0.0
        jd.motorSpeed = 0.05 * Box2D.b2_pi
        jd.maxMotorTorque = 0x1e7f
        jd.enableMotor = True
        self.m_joint = self.world.CreateJoint(jd)

        self.particleSystem.SetRadius(0.025)
        self.particleSystem.SetDamping(0.2)

        pd = b2ParticleGroupDef()
        # pd.flags = TestMain::GetParticleParameterValue()

        shape = b2PolygonShape()
        shape.SetAsBox(0.9, 0.9, b2Vec2(0.0, 1.0), 0.0)

        pd.shape = shape
        pd.color = b2ParticleColor(0, 0, 255, 255)
        group = self.particleSystem.CreateParticleGroup(pd)
        # if (pd.flags & b2_colorMixingParticle):
        # self.ColorParticleGroup(group, 0)

        self.m_time = 0
        self.setZoom(50.0)

    def Step(self, settings):
        super(WaveMachine, self).Step(settings)
        if (settings.hz > 0):
            self.m_time += 1 / settings.hz
        self.m_joint.motorSpeed = (0.05 * math.cos(self.m_time) * Box2D.b2_pi)


if __name__ == "__main__":
    main(WaveMachine)
