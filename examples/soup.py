from math import sqrt
import sys

from .framework import (Framework, Keys, main)
from Box2D import (b2CircleShape, b2FixtureDef, b2PolygonShape, b2Random, b2EdgeShape, b2MassData,
                   b2Vec2, b2_epsilon, b2BodyDef, b2ChainShape, b2ParticleGroupDef, b2ParticleColor)

import Box2D


class Soup (Framework):
    name = "Soup Test"
    description = ''

    m_linear = False

    def __init__(self):
        super(Soup, self).__init__()

        bd = b2BodyDef()
        self.m_ground = self.world.CreateBody(bd)

        shape = b2PolygonShape()
        shape.vertices = [
            b2Vec2(-4, -1),
            b2Vec2(4, -1),
            b2Vec2(4, 0),
            b2Vec2(-4, 0)]
        self.m_ground.CreateFixture(b2FixtureDef(shape=shape, density=0.0))

        shape = b2PolygonShape()
        shape.vertices = [
            b2Vec2(-4, -0.1),
            b2Vec2(-2, -0.1),
            b2Vec2(-2, 2),
            b2Vec2(-4, 3)]
        self.m_ground.CreateFixture(b2FixtureDef(shape=shape, density=0.0))

        shape = b2PolygonShape()
        shape.vertices = [
            b2Vec2(2, -0.1),
            b2Vec2(4, -0.1),
            b2Vec2(4, 3),
            b2Vec2(2, 2)]
        self.m_ground.CreateFixture(b2FixtureDef(shape=shape, density=0.0))

        self.particleSystem.SetRadius(0.025)

        shape = b2PolygonShape()
        shape.SetAsBox(2, 1, b2Vec2(0, 1), 0)
        pd = b2ParticleGroupDef()
        pd.shape = shape
        pd.color = b2ParticleColor(0, 0, 255, 255)
        # pd.flags = TestMain::GetParticleParameterValue();
        group = self.particleSystem.CreateParticleGroup(pd)
        # if (pd.flags & b2_colorMixingParticle):
        # self.ColorParticleGroup(group, 0)

        bd = b2BodyDef()
        bd.type = Box2D.b2_dynamicBody
        body = self.world.CreateBody(bd)
        shape = b2CircleShape()
        shape.pos.Set(0, 0.5)
        shape.radius = 0.1
        body.CreateFixture(b2FixtureDef(shape=shape, density=0.1))
        self.particleSystem.DestroyParticlesInShape(shape, body.transform)

        bd = b2BodyDef()
        bd.type = Box2D.b2_dynamicBody
        body = self.world.CreateBody(bd)
        shape = b2PolygonShape()
        shape.SetAsBox(0.1, 0.1, b2Vec2(-1, 0.5), 0)
        body.CreateFixture(b2FixtureDef(shape=shape, density=0.1))
        self.particleSystem.DestroyParticlesInShape(shape,
                                                    body.transform)

        bd = b2BodyDef()
        bd.type = Box2D.b2_dynamicBody
        body = self.world.CreateBody(bd)
        shape = b2PolygonShape()
        shape.SetAsBox(0.1, 0.1, b2Vec2(1, 0.5), 0.5)
        body.CreateFixture(b2FixtureDef(shape=shape, density=0.1))
        self.particleSystem.DestroyParticlesInShape(shape, body.transform)

        bd = b2BodyDef()
        bd.type = Box2D.b2_dynamicBody
        body = self.world.CreateBody(bd)
        shape = b2EdgeShape()
        shape.vertices = [b2Vec2(0, 2), b2Vec2(0.1, 2.1)]
        body.CreateFixture(b2FixtureDef(shape=shape, density=1))
        massData = b2MassData()
        massData.mass = 0.1
        massData.center = 0.5 * (shape.vertex1 + shape.vertex2)
        massData.I = 0.0
        body.massData = massData

        bd = b2BodyDef()
        bd.type = Box2D.b2_dynamicBody
        body = self.world.CreateBody(bd)
        shape = b2EdgeShape()
        shape.vertices = [b2Vec2(0.3, 2.0), b2Vec2(0.4, 2.1)]
        body.CreateFixture(b2FixtureDef(shape=shape, density=1))
        massData = b2MassData()
        massData.mass = 0.1
        massData.center = 0.5 * (shape.vertex1 + shape.vertex2)
        massData.I = 0.0
        body.massData = massData

        bd = b2BodyDef()
        bd.type = Box2D.b2_dynamicBody
        body = self.world.CreateBody(bd)
        shape = b2EdgeShape()
        shape.vertices = [b2Vec2(-0.3, 2.1), b2Vec2(-0.2, 2.0)]
        body.CreateFixture(b2FixtureDef(shape=shape, density=1))
        massData = b2MassData()
        massData.mass = 0.1
        massData.center = 0.5 * (shape.vertex1 + shape.vertex2)
        massData.I = 0.0
        body.massData = massData

        self.setZoom(50.0)


if __name__ == "__main__":
    main(Soup)
