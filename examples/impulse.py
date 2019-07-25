from math import sqrt
import sys

from .framework import (Framework, Keys, main)
from Box2D import (b2CircleShape, b2FixtureDef, b2PolygonShape, b2Random,
                   b2Vec2, b2_epsilon, b2BodyDef, b2ChainShape, b2ParticleGroupDef, b2ParticleColor)


class Impulse (Framework):
    name = "Impulse Test"
    description = ''

    m_linear = False

    def __init__(self):
        super(Impulse, self).__init__()

        self.kBoxLeft = -2
        self.kBoxRight = 2
        self.kBoxBottom = 0
        self.kBoxTop = 4

        bd = b2BodyDef()
        ground = self.world.CreateBody(bd)

        box = [b2Vec2(self.kBoxLeft, self.kBoxBottom),
               b2Vec2(self.kBoxRight, self.kBoxBottom),
               b2Vec2(self.kBoxRight, self.kBoxTop),
               b2Vec2(self.kBoxLeft, self.kBoxTop)]

        shape = b2ChainShape()
        shape.CreateLoop(box)

        ground.CreateFixture(b2FixtureDef(shape=shape, density=0.0))

        self.particleSystem.SetRadius(0.025)
        self.particleSystem.SetDamping(0.2)

        shape = b2PolygonShape()
        shape.SetAsBox(0.8, 1.0, b2Vec2(0, 1.01), 0)
        pd = b2ParticleGroupDef()
        pd.flags = 1 << 5
        # pd.flags = TestMain::GetParticleParameterValue();
        pd.shape = shape
        pd.color = b2ParticleColor(255, 0, 0, 255)
        group = self.particleSystem.CreateParticleGroup(pd)
        # if pd.flags & b2_colorMixingParticle:
        # self.ColorParticleGroup(group, 0)
        self.setZoom(50.0)

    def ApplyImpulseOrForce(self, direction):
        particleSystem = self.world.GetParticleSystemList()
        particleGroup = particleSystem.GetParticleGroupList()
        numParticles = particleGroup.GetParticleCount()

        if self.m_linear:
            kImpulseMagnitude = 0.005
            impulse = kImpulseMagnitude * direction * numParticles
            particleGroup.ApplyLinearImpulse(impulse)
        else:
            kForceMagnitude = 1.0
            force = kForceMagnitude * direction * numParticles
            particleGroup.ApplyForce(force)

    def Step(self, settings):
        super(Impulse, self).Step(settings)

    def MouseUp(self, p):
        super().MouseUp(p)
        isInsideBox = self.kBoxLeft <= p.x and p.x <= self.kBoxRight and self.kBoxBottom <= p.y and p.y <= self.kBoxTop
        if isInsideBox:
            kBoxCenter = b2Vec2(
                0.5 * (self.kBoxLeft + self.kBoxRight), 0.5 * (self.kBoxBottom + self.kBoxTop))
            direction = p - kBoxCenter
            direction.Normalize()
            self.ApplyImpulseOrForce(direction)

    def Keyboard(self, key):
        if key == Keys.K_l:
            self.m_linear = True
        if key == Keys.K_f:
            self.m_linear = False


if __name__ == "__main__":
    main(Impulse)
